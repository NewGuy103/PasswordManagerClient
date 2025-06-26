import logging
import traceback
import typing

from pathlib import Path

from PySide6.QtCore import QAbstractListModel, QModelIndex, QObject, Qt, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox

from ...version import __version__
from ...localdb.database import MainDatabase
from ...workers import make_worker_thread


if typing.TYPE_CHECKING:
    from ..apps import AppsController


logger: logging.Logger = logging.getLogger("passwordmanager-client")


class RecentDatabasesListModel(QAbstractListModel):
    def __init__(self, /, parent: 'DatabasesTabController' = None):
        super().__init__(parent)
        self.db_ctrl = parent

        self._display_data: list[str] = []
        self._item_data: list[Path] = []
    
    def rowCount(self, /, parent=QModelIndex()):
        return len(self._item_data)

    def data(self, index, /, role):
        if role == Qt.ItemDataRole.UserRole:
            return self._item_data[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._display_data[index.row()]
            return value
        
        return None

    def populate_model(self, recent_databases: list[Path]):
        self.beginResetModel()

        self._display_data.clear()
        self._item_data.clear()

        logger.debug("Cleared all model entries")

        for path in recent_databases:
            self._item_data.append(path)
            self._display_data.append(str(path))

        logger.debug("Added %d entries to model", len(self._item_data))
        self.endResetModel()


class DatabasesTabController(QObject):
    databaseLoaded = Signal(MainDatabase)

    def __init__(self, app_parent: 'AppsController'):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui
        self.ui.databasesTitleLabel.setText(f"PasswordManager - Client: {__version__}")

        self.ui.databasesNewDatabaseButton.clicked.connect(self.new_database_clicked)
        self.ui.databasesOpenDatabaseButton.clicked.connect(self.open_database_clicked)

        self.recent_databases_model = RecentDatabasesListModel(parent=self)
        self.ui.recentlyOpenedDatabasesListView.setModel(self.recent_databases_model)

        self.recent_databases_model.populate_model(self.app_parent.mw_parent.app_settings.recent_databases)
        self.ui.recentlyOpenedDatabasesListView.doubleClicked.connect(self.recent_databases_triggered)

    @Slot()
    def new_database_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self.mw_parent, "Save database to file",
            "untitled.db", "Database Files (*.db)"
        )
        if not file_name:
            return
        
        path = Path(file_name)

        settings = self.app_parent.mw_parent.app_settings

        # Sort it to the top
        if path in settings.recent_databases:
            settings.recent_databases.remove(path)
        
        settings.recent_databases.append(path)
        settings.save_settings()

        self._load_database(path)
        self.ui.statusbar.showMessage('Databases - Creating new database', timeout=5000)
    
    @Slot()
    def open_database_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self.mw_parent, "Open database",
            "", "Database Files (*.db)"
        )
        if not file_name:
            return
        
        path = Path(file_name)

        settings = self.app_parent.mw_parent.app_settings

        # Sort it to the top
        if path in settings.recent_databases:
            settings.recent_databases.remove(path)
        
        settings.recent_databases.append(path)
        settings.save_settings()
        
        self._load_database(path)
        self.ui.statusbar.showMessage('Databases - Opening database', timeout=5000)

    @Slot()
    def recent_databases_triggered(self, index: QModelIndex):
        item: Path = index.data(Qt.ItemDataRole.UserRole)
        if not item.is_file():
            QMessageBox.warning(
                self.mw_parent,
                "PasswordManager - Client",
                "The database selected has been moved/deleted.",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok
            )
            settings = self.app_parent.mw_parent.app_settings
            settings.recent_databases.remove(item)

            settings.save_settings()
            return
        
        self._load_database(item)
        self.ui.statusbar.showMessage('Databases - Opening recently used database', timeout=5000)

    @Slot(Exception)
    def worker_exc_received(self, exc: Exception):
        tb: str = ''.join(traceback.format_exception(exc, limit=1))

        QMessageBox.warning(
            self.mw_parent,
            "PasswordManager - Client",
            f"Unable to load database. Check the log file for more details. Traceback:\n\n{tb}",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok
        )
        logger.error("Failed to load database due to exception:", exc_info=exc)
    
    def _load_database(self, path: Path):
        self.db = MainDatabase()
        make_worker_thread(lambda: self.db.setup(path), self.database_after_setup, self.worker_exc_received)

        self.ui.statusbar.showMessage('Databases - Setting up database', timeout=5000)

    @Slot(None)
    def database_after_setup(self):
        self.databaseLoaded.emit(self.db)
        self.ui.statusbar.showMessage("Databases - Loaded database", timeout=5000)
