import logging
import traceback
import typing

import keyring

from functools import partial

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QMessageBox

from ...models import SyncInfo, SavedSyncInfo
from ...workers import make_worker_thread

from ...localdb.database import MainDatabase
from ...serversync.client import SyncClient

if typing.TYPE_CHECKING:
    from ..apps import AppsController


logger: logging.Logger = logging.getLogger("passwordmanager-client")


class SyncClientLoader(QObject):
    clientLoaded = Signal(SyncClient)
    loadWithoutSync = Signal()

    def __init__(self, app_parent: "AppsController"):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui
        self.db: MainDatabase = None

    @Slot(MainDatabase)
    def database_loaded(self, db: MainDatabase):
        self.db = db
        make_worker_thread(self.db.syncinfo.get_sync_info, self.db_check_sync_enabled, self.worker_exc_received)

        self.ui.statusbar.showMessage("SyncClient - Checking if sync is enabled", timeout=5000)

    @Slot(SyncInfo)
    def db_check_sync_enabled(self, data: SyncInfo):
        logger.info(data)
        if not data.sync_enabled:
            self.loadWithoutSync.emit()
            self.ui.statusbar.showMessage("SyncClient - Sync is disabled, continuing...", timeout=5000)
            return

        access_token = keyring.get_password("newguy103-passwordmanager", f"{data.username}={str(data.server_url)}")
        saved_sync_info = SavedSyncInfo(
            username=data.username,
            server_url=data.server_url,
            access_token=access_token,
            sync_enabled=data.sync_enabled,
        )

        self.sync_client = SyncClient()
        func = partial(self.sync_client.setup, saved_sync_info)

        make_worker_thread(func, self.sync_client_after_setup, self.worker_exc_received)

    @Slot(None)
    def sync_client_after_setup(self):
        self.clientLoaded.emit(self.sync_client)
        self.ui.statusbar.showMessage("SyncClient - Loaded sync client", timeout=5000)

    @Slot(Exception)
    def worker_exc_received(self, exc: Exception):
        tb: str = "".join(traceback.format_exception(exc, limit=1))

        QMessageBox.warning(
            self.mw_parent,
            "PasswordManager - Client",
            f"Server sync cannot be loaded, falling back to no sync. Traceback:\n\n{tb}",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )
        logger.error("Failed to setup sync client due to exception:", exc_info=exc)
        self.loadWithoutSync.emit()
