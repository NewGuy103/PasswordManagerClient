import typing

from PySide6.QtCore import QObject, Slot

from .tabs.databases import DatabasesTabController
from .tabs.passwords import PasswordsTabController
from .tabs.settings import SettingsTabController
from .tabs.sync_client import SyncClientLoader

if typing.TYPE_CHECKING:
    from ..main import MainWindow


class AppsController(QObject):
    def __init__(self, mw_parent: "MainWindow"):
        super().__init__(mw_parent)

        self.mw_parent = mw_parent
        self.ui = mw_parent.ui

        self.ui.appTabWidget.setCurrentIndex(0)  # databases tab
        self.ui.appTabWidget.setTabEnabled(1, False)  # disable passwords by default

        self.setup()

    def setup(self):
        self.pw_tab = PasswordsTabController(self)
        self.db_tab = DatabasesTabController(self)

        self.settings_tab = SettingsTabController(self)
        self.sync_loader = SyncClientLoader(self)

        self.db_tab.databaseLoaded.connect(self.settings_tab.database_loaded)
        self.db_tab.databaseLoaded.connect(self.pw_tab.database_loaded)

        self.db_tab.databaseLoaded.connect(self.sync_loader.database_loaded)
        self.db_tab.databaseLoaded.connect(self.wait_for_sync_load)

        self.sync_loader.clientLoaded.connect(self.settings_tab.client_loaded)
        self.sync_loader.clientLoaded.connect(self.pw_tab.client_loaded)

        self.sync_loader.clientLoaded.connect(self.enable_passwords_tab)

    @Slot()
    def wait_for_sync_load(self):
        self.ui.appTabWidget.setTabEnabled(1, False)

        # Disable while waiting for sync load to complete
        self.ui.databasesTab.setDisabled(True)

    @Slot()
    def enable_passwords_tab(self):
        self.ui.appTabWidget.setTabEnabled(0, False)  # disable databases tab
        self.ui.appTabWidget.setTabEnabled(1, True)  # enable passwords

        self.ui.appTabWidget.setCurrentIndex(1)  # passwords
