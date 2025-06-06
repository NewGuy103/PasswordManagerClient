import logging
import typing
import uuid
from functools import partial

from PySide6.QtCore import QAbstractItemModel, QAbstractListModel, QModelIndex, QObject, Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QDialog, QHeaderView, QMenu, QMessageBox

from ...localdb.database import database
from ...localdb.dbtables import PasswordEntry
from ...models import AddPasswordEntry, PasswordEntryData
from ...ui.add_password_entry_dialog import Ui_AddPasswordEntryDialog
from ...workers import make_worker_thread

if typing.TYPE_CHECKING:
    from ..apps import AppsController


logger: logging.Logger = logging.getLogger("passwordmanager-client")


# TODO: If possible, make this a table model so i dont rely on string lists
class PasswordEntriesModel(QAbstractListModel):
    def __init__(self, /, parent: 'PasswordEntriesViewController' = None):
        super().__init__(parent)
        self.pw_ctrl = parent

        self.worker_exc_received = parent.pw_parent.worker_exc_received

        self.display_entries: list[str] = []  # list[str] for now
        self.item_entries: list[PasswordEntryData] = []  # table is probably better
    
    def load_data_for_group(self, group_id: uuid.UUID):
        @Slot(list)
        def query_complete(entries: list[PasswordEntryData]):
            self.beginResetModel()

            self.item_entries.clear()
            self.display_entries.clear()

            for data in entries:
                self.item_entries.append(data)
                self.display_entries.append(f"[{data.entry_id}] Entry name: {data.entry_name}"
                                    f" - {data.username} | {data.password} | {data.url}")

            self.endResetModel()

        func = partial(database.entries.get_entries_by_group, group_id)
        make_worker_thread(func, data_func=query_complete, exc_callback=self.worker_exc_received)

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if role == Qt.ItemDataRole.DisplayRole:
            text = self.display_entries[index.row()]
            return text
        
        if role == Qt.ItemDataRole.UserRole:
            item: PasswordEntryData = self.item_entries[index.row()]
            return item
        
        return None
    
    def rowCount(self, /, index: QModelIndex):
        return len(self.item_entries)
    
    def add_entry(self, group_id: uuid.UUID, data: AddPasswordEntry) -> None:
        @Slot()
        def create_complete(entry: PasswordEntryData):
            self.item_entries.append(entry)
            self.display_entries.append(f"[{entry.entry_id}] Entry name: {entry.entry_name} - "
                                        f"{entry.username} | {entry.password} | {entry.url}")
            self.layoutChanged.emit()

            logger.info("Created entry '%s'", entry.entry_id)
        
        func = partial(
            database.entries.create_entry, group_id,
            data.entry_name, data.username, data.password, data.url
        )
        make_worker_thread(func, data_func=create_complete, exc_callback=self.worker_exc_received)
    
    def delete_entry(self, parent: QModelIndex, entry_id: uuid.UUID):
        @Slot()
        def delete_complete():
            del self.item_entries[parent.row()]
            del self.display_entries[parent.row()]

            self.layoutChanged.emit()
            logger.info("Deleted entry ID '%s'", entry_id)
        
        func = partial(database.entries.delete_entry_by_id, entry_id)
        make_worker_thread(func, data_func=delete_complete, exc_callback=self.worker_exc_received)


# TODO: Implement tree model using example from PySide6
class PasswordGroupsModel(QAbstractItemModel):
    ...


class PasswordsTabController(QObject):
    def __init__(self, app_parent: 'AppsController'):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui

        # Variables
        self.current_group_id: uuid.UUID = None

        # Controllers
        self.ui_setup()
        self.entries_view_ctrl = PasswordEntriesViewController(self)

    def ui_setup(self):
        # TODO: Uncomment after implementing item model
        # self.ui.passwordGroupsTreeView.header().setStretchLastSection(False)

        # for column in range(self.ui.passwordGroupsTreeView.model().columnCount()):
        #     self.ui.passwordGroupsTreeView.header().setSectionResizeMode(
        #         column, QHeaderView.ResizeMode.ResizeToContents
        #     )
        
        # self.ui.passwordGroupsTreeView.expandAll()

        # TODO: Make this usable with many groups and root group, and use a thread
        self.current_group_id = database.groups.get_root_group_id()

    @Slot(Exception)
    def worker_exc_received(self, exc: Exception):
        logger.error("Exception when running worker:", exc_info=exc)


class PasswordEntriesViewController(QObject):
    def __init__(self, pw_parent: PasswordsTabController):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui
    
        self.entries_model = PasswordEntriesModel(parent=self)
        self.ui.passwordEntriesListView.setModel(self.entries_model)

        self.ui.passwordEntriesListView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.passwordEntriesListView.customContextMenuRequested.connect(self.context_menu_event)

        self.entries_model.load_data_for_group(self.pw_parent.current_group_id)
    
    @Slot()
    def context_menu_event(self, pos):
        context = QMenu(self.mw_parent)

        # Icons
        list_add_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        list_remove_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))

        # Actions
        add_entry_action = QAction("Add entry", self, icon=list_add_icon)
        remove_entry_action = QAction("Remove entry", self, icon=list_remove_icon)

        # Triggers
        add_entry_action.triggered.connect(self.add_password_entry)
        context.addAction(add_entry_action)

        # Item-dependent triggers
        indexes = self.ui.passwordEntriesListView.selectedIndexes()
        if indexes:
            index = indexes[0]
            current_item: PasswordEntryData = self.entries_model.data(index, Qt.ItemDataRole.UserRole)

            remove_entry_action.triggered.connect(lambda: self.delete_password_entry(index, current_item))

        # Item-dependent actions
        if indexes:
            context.addAction(remove_entry_action)
        
        context.exec(self.ui.passwordEntriesListView.mapToGlobal(pos))

    @Slot()
    def add_password_entry(self):
        # TODO: Add a way to get the group_id of the currently selected group
        dialog = AddPasswordEntryDialog(self)

        @Slot(AddPasswordEntry)
        def dialog_accepted(data: AddPasswordEntry):
            # TODO: Make this safer, if current_group_id changes it may add to the wrong group
            self.entries_model.add_entry(self.pw_parent.current_group_id, data)
        
        dialog.dataComplete.connect(dialog_accepted)
        dialog.exec()

        dialog.deleteLater()

    def delete_password_entry(self, index: QModelIndex, item: PasswordEntryData):
        self.entries_model.delete_entry(index, item.entry_id)
        self.ui.passwordEntriesListView.clearSelection()


class AddPasswordEntryDialog(QDialog):
    dataComplete = Signal(AddPasswordEntry)
    def __init__(self, /, parent: PasswordEntriesViewController):
        super().__init__(parent.mw_parent)
        self.ui = Ui_AddPasswordEntryDialog()
        
        self.pw_parent = parent
        self.ui.setupUi(self)
    
    def accept(self):
        entry_name = self.ui.entryNameLineEdit.text()
        username = self.ui.usernameLineEdit.text()

        password = self.ui.passwordLineEdit.text()
        url = self.ui.urlLineEdit.text()

        data = AddPasswordEntry(
            entry_name=entry_name,
            username=username,
            password=password,
            url=url
        )

        self.dataComplete.emit(data)
        return super().accept()
