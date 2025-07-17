import logging
import traceback
import typing

import keyring

from functools import partial

from pydantic import HttpUrl, TypeAdapter, ValidationError
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox, QAbstractButton

from ...version import __version__
from ...localdb.database import MainDatabase
from ...ui.edit_sync_info_dialog import Ui_EditSyncInfoDialog

from ...client import Client
from ...client.api.auth import token_login_api_auth_token_post as token_login
from ...client.models import AccessTokenError, AccessTokenResponse
from ...client.models import BodyTokenLoginApiAuthTokenPost as TokenLoginBody
from ...client.types import Response

from ...models import SyncInfo, TestSyncAuth, SavedSyncInfo
from ...config import app_file_paths, LogLevels
from ...workers import make_worker_thread

if typing.TYPE_CHECKING:
    from ..apps import AppsController


logger: logging.Logger = logging.getLogger("passwordmanager-client")


class SettingsTabController(QObject):
    testAuthComplete = Signal(AccessTokenResponse)
    testAuthFailed = Signal()

    def __init__(self, app_parent: "AppsController"):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui
        self.edit_syncinfo_dialog = EditSyncInfoDialog(self)

        self.ui_setup()

    def ui_setup(self):
        self.ui.databaseSettingsGroupBox.setEnabled(False)
        self.ui.clientVersionLabel.setText(f"Client version: {__version__}")

        loglevel_name = self.mw_parent.app_settings.log_level.name.capitalize()
        self.ui.logLevelComboBox.setCurrentText(loglevel_name)

        # Add slot only after first run
        self.ui.logLevelComboBox.currentTextChanged.connect(self.loglevel_changed)
        self.ui.logFilePathLabel.setText(f"Log file: {app_file_paths.log_file}")

        self.ui.syncInfoServerURLLabel.setText(f"Server URL: {None}")
        self.ui.syncInfoUsernameLabel.setText(f"Username: {None}")

        self.ui.syncInfoEditButton.clicked.connect(self.edit_syncinfo_clicked)
        self.edit_syncinfo_dialog.testAuthRequested.connect(self.test_auth_request)

        self.edit_syncinfo_dialog.dataSaveRequested.connect(self.save_syncinfo)
        self.edit_syncinfo_dialog.syncEnabledToggled.connect(self.toggle_sync_enabled)

        self.testAuthComplete.connect(self.edit_syncinfo_dialog.test_auth_complete)
        self.testAuthFailed.connect(self.edit_syncinfo_dialog.test_auth_failed)

    @Slot(MainDatabase)
    def database_loaded(self, database: MainDatabase):
        self.db = database
        make_worker_thread(self.db.syncinfo.get_sync_info, self.sync_info_returned, self.worker_exc_received)

    @Slot(SyncInfo)
    def sync_info_returned(self, sync_info: SyncInfo):
        self.syncinfo = sync_info
        self.ui.databaseSettingsGroupBox.setEnabled(True)

        self.ui.syncInfoUsernameLabel.setText(f"Username: {sync_info.username or None}")
        self.ui.syncInfoServerURLLabel.setText(f"Server URL: {sync_info.server_url}")

    @Slot(str)
    def loglevel_changed(self, log_level: str):
        match log_level.lower():
            case LogLevels.debug.name:
                level = logging.DEBUG
            case LogLevels.info.name:
                level = logging.INFO
            case LogLevels.warning.name:
                level = logging.WARNING
            case LogLevels.error.name:
                level = logging.ERROR
            case LogLevels.critical.name:
                level = logging.CRITICAL
            case _:
                level = logging.INFO

        self.mw_parent.app_settings.log_level = level
        self.mw_parent.app_settings.save_settings()

        logger.setLevel(level)
        self.ui.statusbar.showMessage(f"Settings - Set logging level to '{log_level}'", timeout=5000)

    @Slot()
    def edit_syncinfo_clicked(self):
        self.edit_syncinfo_dialog.reset_data(self.syncinfo)
        self.edit_syncinfo_dialog.show()

    @Slot(TestSyncAuth)
    def test_auth_request(self, data: TestSyncAuth):
        client = Client(str(data.server_url), raise_on_unexpected_status=True)
        body = TokenLoginBody(grant_type="password", username=data.username, password=data.password)

        func = partial(token_login.sync_detailed, client=client, body=body)

        self.ui.syncInfoEditButton.setEnabled(False)
        make_worker_thread(func, self.test_auth_complete, self.test_auth_failed)

    @Slot()
    def test_auth_failed(self, exc: Exception):
        tb: str = "".join(traceback.format_exception(exc, limit=1))
        QMessageBox.critical(
            self.mw_parent,
            "PasswordManager - Client",
            f"Could not login to server, check log file for more information. Traceback: \n\n{tb}",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )
        logger.exception("Could not fetch Authorization header:", exc_info=exc)

        self.ui.syncInfoEditButton.setEnabled(True)
        self.testAuthFailed.emit()

    @Slot()
    def test_auth_complete(self, resp: Response[AccessTokenResponse | AccessTokenError]):
        data = resp.parsed
        if data is None:
            QMessageBox.warning(
                self.mw_parent,
                "PasswordManager - Client",
                f"Invalid content from server when logging in: {resp.content.decode('utf-8')}",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            self.testAuthFailed.emit()
            return

        self.ui.statusbar.showMessage("Settings - HTTP response received", timeout=5000)
        if isinstance(data, AccessTokenError):
            QMessageBox.information(
                self.mw_parent,
                "PasswordManager - Client",
                f"Invalid credentials were passed:\n{data.error} - {data.error_description}",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            self.testAuthFailed.emit()
            return

        logger.debug("Authorization header received")
        self.ui.syncInfoEditButton.setEnabled(True)

        self.testAuthComplete.emit(data)

    @Slot(SavedSyncInfo)
    def save_syncinfo(self, data: SavedSyncInfo):
        func = partial(self.db.syncinfo.set_sync_info, data.username, data.server_url, data.sync_enabled)
        keyring.set_password("newguy103-passwordmanager", f"{data.username}={str(data.server_url)}", data.access_token)
        make_worker_thread(func, self.database_save_syncinfo_complete, self.worker_exc_received)

    @Slot(SyncInfo)
    def database_save_syncinfo_complete(self, data: SyncInfo):
        self.syncinfo = data

        self.ui.syncInfoUsernameLabel.setText(f"Username: {data.username or None}")
        self.ui.syncInfoServerURLLabel.setText(f"Server URL: {data.server_url}")

    @Slot(bool)
    def toggle_sync_enabled(self, sync_enabled: bool):
        func = partial(self.db.syncinfo.toggle_sync_enabled, sync_enabled)
        make_worker_thread(func, self.database_toggle_sync_complete, self.worker_exc_received)

    @Slot(SyncInfo)
    def database_toggle_sync_complete(self, data: SyncInfo):
        self.syncinfo = data
        self.ui.statusbar.showMessage("Settings - Toggled sync enabled", timeout=5000)

    @Slot(Exception)
    def worker_exc_received(self, exc: Exception):
        tb: str = "".join(traceback.format_exception(exc, limit=1))

        QMessageBox.warning(
            self.mw_parent,
            "PasswordManager - Client",
            f"An error occured. Check the log file for more details. Traceback:\n\n{tb}",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )
        logger.error("Settings - Exception when running worker:", exc_info=exc)


class EditSyncInfoDialog(QDialog):
    testAuthRequested = Signal(TestSyncAuth)
    dataSaveRequested = Signal(SavedSyncInfo)
    syncEnabledToggled = Signal(bool)

    def __init__(self, parent: SettingsTabController):
        super().__init__(parent.mw_parent)
        self.settings_parent = parent

        self.ui = Ui_EditSyncInfoDialog()
        self.ui.setupUi(self)

        self.ui.serverURLLineEdit.textEdited.connect(self.serverurl_textedited)
        self.ui.dialogButtonBox.clicked.connect(self.dialog_button_clicked)

        self.ui.testAuthButton.clicked.connect(self.test_auth_clicked)
        self._test_auth_successful: bool = False

        self._authdata: AccessTokenResponse | None = None

    def reset_data(self, data: SyncInfo):
        self._test_auth_successful: bool = False
        self._authdata: AccessTokenResponse | None = None

        self.syncinfo = data

        # Reset UI
        self.ui.usernameLineEdit.setEnabled(True)
        self.ui.serverURLLineEdit.setEnabled(True)

        self.ui.passwordLineEdit.setEnabled(True)
        self.ui.usernameLineEdit.setText(data.username)

        self.ui.serverURLLineEdit.setText(str(data.server_url) if data.server_url else "")
        self.ui.passwordLineEdit.setText("")

        self.ui.syncEnabledCheckBox.setChecked(data.sync_enabled)
        btn = self.ui.dialogButtonBox.button(QDialogButtonBox.StandardButton.Save)

        self.ui.testAuthButton.setEnabled(True)
        btn.setEnabled(True)

    def _compare_values_changed(self):
        username = self.ui.usernameLineEdit.text()
        server_url = self.ui.serverURLLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        actual_url = str(self.syncinfo.server_url) if self.syncinfo.server_url else ""

        if username != self.syncinfo.username:
            return True

        if server_url != actual_url:
            return True

        if password:
            return True

        return False

    def accept(self):
        if self._compare_values_changed() and not self._test_auth_successful:
            QMessageBox.information(
                self,
                "PasswordManager - Client",
                (
                    "Changing sync information requires a request "
                    "to re-authenticate with the server. Please test authorization "
                    "before saving sync information."
                ),
            )
            return

        if self._authdata and self._test_auth_successful:
            username = self.ui.usernameLineEdit.text()
            server_url = self.ui.serverURLLineEdit.text()

            save_syncinfo = SavedSyncInfo(
                username=username,
                server_url=server_url,
                access_token=self._authdata.access_token,
                sync_enabled=self.ui.syncEnabledCheckBox.isChecked(),
            )
            self.dataSaveRequested.emit(save_syncinfo)

        sync_enabled = self.ui.syncEnabledCheckBox.isChecked()
        if self.syncinfo.sync_enabled != sync_enabled and not self._authdata:
            self.syncEnabledToggled.emit(sync_enabled)

        return super().accept()

    def reject(self):
        if self._authdata and self._test_auth_successful:
            btn = QMessageBox.question(self, "PasswordManager - Client", "Discard changes to sync info?")
            if btn == QMessageBox.StandardButton.No:
                return

        return super().reject()

    @Slot()
    def test_auth_clicked(self):
        username = self.ui.usernameLineEdit.text()
        server_url = self.ui.serverURLLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if not username or not server_url or not password:
            QMessageBox.warning(
                self,
                "PasswordManager - Client",
                "Enter a username, server URL and password before testing authorization.",
            )
            return

        # Disable changing of data while waiting and on success
        self.ui.usernameLineEdit.setEnabled(False)
        self.ui.serverURLLineEdit.setEnabled(False)

        self.ui.passwordLineEdit.setEnabled(False)

        test_sync_auth = TestSyncAuth(username=username, server_url=server_url, password=password)
        self.testAuthRequested.emit(test_sync_auth)

    @Slot()
    def test_auth_complete(self, data: AccessTokenResponse):
        self._test_auth_successful: bool = True
        self._authdata = data

        QMessageBox.information(
            self, "PasswordManager - Client", "Login complete, you can now save the sync information to the database."
        )

    @Slot()
    def test_auth_failed(self):
        # Re-enable line edits
        self.ui.usernameLineEdit.setEnabled(True)
        self.ui.serverURLLineEdit.setEnabled(True)

        self.ui.passwordLineEdit.setEnabled(True)

    @Slot()
    def dialog_button_clicked(self, button: QAbstractButton):
        role = self.ui.dialogButtonBox.buttonRole(button)

        if role == QDialogButtonBox.ButtonRole.DestructiveRole:
            self.reject()

    @Slot()
    def serverurl_textedited(self, text: str):
        ta = TypeAdapter(HttpUrl)
        btn = self.ui.dialogButtonBox.button(QDialogButtonBox.StandardButton.Save)

        test_auth_btn = self.ui.testAuthButton
        try:
            if text:
                ta.validate_python(text)
        except ValidationError:
            test_auth_btn.setEnabled(False)
            btn.setEnabled(False)
            return

        test_auth_btn.setEnabled(True)
        btn.setEnabled(True)
