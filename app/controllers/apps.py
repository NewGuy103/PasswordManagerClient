import typing

from PySide6.QtCore import QObject

from .tabs.passwords import PasswordsTabController
from .tabs.databases import DatabasesTabController
from .tabs.settings import SettingsTabController

if typing.TYPE_CHECKING:
    from ..main import MainWindow


class AppsController(QObject):
    def __init__(self, mw_parent: 'MainWindow'):
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

        self.db_tab.databaseLoaded.connect(self.settings_tab.database_loaded)
        self.db_tab.databaseLoaded.connect(self.pw_tab.database_loaded)

        self.db_tab.databaseWithSyncLoaded.connect(self.settings_tab.database_loaded)
        self.db_tab.databaseWithSyncLoaded.connect(self.pw_tab.database_loaded)
