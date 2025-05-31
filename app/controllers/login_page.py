import traceback
import typing
from functools import partial

import httpx
import keyring
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QMessageBox

from ..client import Client
from ..client.api.auth import token_login_api_auth_token_post as token_login
from ..client.models import AccessTokenError, AccessTokenResponse
from ..client.models import BodyTokenLoginApiAuthTokenPost as TokenLoginBody
from ..client.types import Response
from ..config import AvailableLogins
from ..workers import make_worker_thread

if typing.TYPE_CHECKING:
    from ..main import MainWindow


class LoginController(QObject):
    login_done = Signal(AvailableLogins)
    
    def __init__(self, mw_parent: 'MainWindow'):
        super().__init__(mw_parent)

        self.mw_parent = mw_parent
        self.ui = mw_parent.ui

        self.provided_username = None

        self.ui.loginButton.clicked.connect(self.login_start)
        self.ui.serverURILineEdit.setFocus()

    def check_saved_credentials(self):
        """Only check for saved keyring credentials, not verify, leave that to the dashboard"""
        
        login_models = self.mw_parent.app_settings.logins

        # No logins in config file
        if not login_models:
            return
        
        for login_model in login_models:
            if not login_model.is_default:
                continue

            auth_header = keyring.get_password(
                'newguy103-syncserver',
                login_model.username
            )

            if auth_header:
                self.login_done.emit(login_model)
                return

        # No default login, make the first login default
        first_login = login_models[0]
        auth_header = keyring.get_password(
            'newguy103-passwordmanager',
            first_login.username
        )

        if auth_header:
            self.login_done.emit(first_login)
            login_models[0].is_default = True

            self.mw_parent.app_settings.save_settings()
            return

    @Slot()
    def login_start(self):
        server_url = self.ui.serverURILineEdit.text()
        if not server_url:
            QMessageBox.warning(
                self.mw_parent, 
                "PasswordManager - Client",
                "Enter the server hostname where PasswordManager is running.",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok
            )
            return
        
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if not username or not password:
            QMessageBox.warning(
                self.mw_parent,
                "PasswordManager - Client",
                "Enter a username and password.",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return
        
        client = Client(base_url=server_url, raise_on_unexpected_status=True)
        body = TokenLoginBody(
            grant_type='password',
            username=username,
            password=password
        )

        func = partial(
            token_login.sync_detailed,
            client=client, body=body
        )
        
        self._worker_refs = make_worker_thread(func, self.on_worker_complete, self.on_worker_exc)

        self.provided_username: str = username
        self.provided_server_url: str = server_url

        self.ui.statusbar.showMessage('Auth - Sent HTTP request for token', timeout=30000)
    
    @Slot()
    def on_worker_complete(self, resp: Response[AccessTokenResponse | AccessTokenError]):
        data = resp.parsed
        if data is None:
            QMessageBox.information(
                self.mw_parent,
                "PasswordManager - Client",
                f"Invalid content from server: {resp.content}",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return
        
        self.ui.statusbar.showMessage('Auth - HTTP response received', timeout=5000)
        if isinstance(data, AccessTokenError):
            QMessageBox.information(
                self.mw_parent,
                "PasswordManager - Client",
                f"Invalid credentials were passed:\n{data.error} - {data.error_description}",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return
        
        # First user
        if len(self.mw_parent.app_settings.logins) == 0:
            is_default = True
        else:
            is_default = False
        
        login_model = AvailableLogins(
            username=self.provided_username,
            server_url=self.provided_server_url,
            is_default=is_default
        )

        # Dont add existing login, only overwrite the keyring value
        for existing_login in self.mw_parent.app_settings.logins:
            if login_model.username != existing_login.username:
                continue
            
            if login_model.server_url != existing_login.server_url:
                continue

            keyring.set_password(
                'newguy103-passwordmanager', 
                self.provided_username, 
                data.access_token
            )
            self.login_done.emit(login_model)
            return
        
        keyring.set_password(
            'newguy103-passwordmanager', 
            self.provided_username, 
            data.access_token
        )
        self.mw_parent.app_settings.logins.append(login_model)
        self.mw_parent.app_settings.save_settings()

        self.login_done.emit(login_model)
        return
    
    @Slot(Exception)
    def on_worker_exc(self, exc: Exception):
        self.ui.statusbar.showMessage('Auth - HTTP request failed', timeout=5000)
        tb: str = ''.join(traceback.format_exception(exc, limit=1))

        match exc:
            case httpx.InvalidURL() | httpx.UnsupportedProtocol():
                QMessageBox.warning(
                    self.mw_parent,
                    "PasswordManager - Client",
                    f"Invalid HTTP host passed. Details:\n\n{tb}",
                    buttons=QMessageBox.StandardButton.Ok,
                    defaultButton=QMessageBox.StandardButton.Ok
                )
            case httpx.HTTPError():
                QMessageBox.warning(
                    self.mw_parent,
                    "PasswordManager - Client",
                    f"An HTTP error occured.\nDetails:\n\n{tb}",
                    buttons=QMessageBox.StandardButton.Ok,
                    defaultButton=QMessageBox.StandardButton.Ok,
                )
            case _:
                QMessageBox.critical(
                    self.mw_parent,
                    "PasswordManager - Client",
                    f"An unexpected error occured, check the log file for details.\nTraceback:\n\n{tb}"
                )
        return
