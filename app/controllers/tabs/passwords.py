import logging
import typing
import uuid
from functools import partial

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QObject, Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QHeaderView, QMenu, QMessageBox

from ...localdb.database import database
from ...models import AddPasswordEntry, AddPasswordGroup, GroupParentData, PasswordEntryData
from ...ui.add_password_entry_dialog import Ui_AddPasswordEntryDialog
from ...ui.add_password_group_dialog import Ui_AddPasswordGroupDialog
from ...workers import make_worker_thread

if typing.TYPE_CHECKING:
    from ..apps import AppsController


logger: logging.Logger = logging.getLogger("passwordmanager-client")


class PasswordEntriesTableModel(QAbstractTableModel):
    def __init__(self, /, parent: 'PasswordEntriesViewController' = None):
        super().__init__(parent)
        self.pw_ctrl = parent

        self._display_data: list[list[str]] = []
        self._item_data: list[PasswordEntryData] = []

        self._col_headers: list[str] = ['Entry Name', 'Username', 'URL']
    
    def rowCount(self, /, parent=QModelIndex()):
        return len(self._item_data)

    def columnCount(self, /, parent=QModelIndex()):
        return len(self._col_headers)
    
    def data(self, index, /, role):
        if role == Qt.ItemDataRole.UserRole:
            return self._item_data[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self._display_data[index.row()][index.column()]
        
        return None
    
    def headerData(self, section, orientation, /, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == Qt.Orientation.Horizontal:
            return self._col_headers[section]

        if orientation == Qt.Orientation.Vertical:
            return super().headerData(section, orientation, role)

    def load_entries(self, entries: list[PasswordEntryData]):
        self.beginResetModel()

        self._display_data.clear()
        self._item_data.clear()

        logger.debug("Cleared all model entries")

        for entry in entries:
            display_data = [entry.entry_name, entry.username, entry.url]
            self._display_data.append(display_data)

            self._item_data.append(entry)

        logger.debug("Added %d entries to model", len(self._item_data))
        self.endResetModel()
    
    def add_entry(self, entry: PasswordEntryData):
        display_data = [entry.entry_name, entry.username, entry.url]

        self._item_data.append(entry)
        self._display_data.append(display_data)

        self.layoutChanged.emit()
    
    def delete_entry(self, index: QModelIndex):
        del self._item_data[index.row()]
        del self._display_data[index.row()]

        self.layoutChanged.emit()


class PasswordsTabController(QObject):
    def __init__(self, app_parent: 'AppsController'):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui
        make_worker_thread(database.groups.get_children_of_root, self.setup, self.worker_exc_received)

    @Slot(GroupParentData)
    def setup(self, data: GroupParentData):
        self.current_group = data

        # Controllers
        self.entries_view_ctrl = PasswordEntriesViewController(self)
        self.groups_view_ctrl = PasswordGroupsItemController(self)

        self.groups_view_ctrl.groupChanged.connect(self.entries_view_ctrl.reload_entries)

    @Slot(Exception)
    def worker_exc_received(self, exc: Exception):
        logger.error("Exception when running worker:", exc_info=exc)


class PasswordEntriesViewController(QObject):
    def __init__(self, pw_parent: PasswordsTabController):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui
    
        self.entries_model = PasswordEntriesTableModel(parent=self)
        self.ui.passwordEntriesTableView.setModel(self.entries_model)

        self.setup()
        
    def setup(self):
        header = self.ui.passwordEntriesTableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        header.setStretchLastSection(True)

        self.ui.passwordEntriesTableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.passwordEntriesTableView.customContextMenuRequested.connect(self.context_menu_event)
    
    @Slot()
    def reload_entries(self, group: GroupParentData):
        self.current_group = group
        func = partial(database.entries.get_entries_by_group, group.group_id)

        make_worker_thread(func, self.model_reload_entries, self.pw_parent.worker_exc_received)
        logger.info("Reloading entries for group '%s'", group.group_name)
    
    @Slot()
    def model_reload_entries(self, entries: list[PasswordEntryData]):
        logger.info("Fetched %d entries", len(entries))
        self.entries_model.load_entries(entries)
    
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
        indexes = self.ui.passwordEntriesTableView.selectedIndexes()
        if indexes:
            # Get only the first index, because the QTableView uses the SelectRows behavior
            index = indexes[0]
            current_item: PasswordEntryData = self.entries_model.data(index, Qt.ItemDataRole.UserRole)

            remove_entry_action.triggered.connect(lambda: self.delete_password_entry(index, current_item))

        # Item-dependent actions
        if indexes:
            context.addAction(remove_entry_action)
        
        context.exec(self.ui.passwordEntriesTableView.mapToGlobal(pos))

    @Slot()
    def add_password_entry(self):
        dialog = AddPasswordEntryDialog(self)

        @Slot(AddPasswordEntry)
        def dialog_accepted(data: AddPasswordEntry):
            func = partial(
                database.entries.create_entry, self.current_group.group_id,
                data.entry_name, data.username, data.password, data.url
            )
            make_worker_thread(func, self.model_add_password_entry, self.pw_parent.worker_exc_received)
    
        dialog.dataComplete.connect(dialog_accepted)
        dialog.exec()

        dialog.deleteLater()

    @Slot()
    def model_add_password_entry(self, entry: PasswordEntryData):
        logger.info("Adding entry '%s'", entry.entry_name)
        self.entries_model.add_entry(entry)
    
    def delete_password_entry(self, index: QModelIndex, item: PasswordEntryData):
        btn = QMessageBox.information(
            self.mw_parent,
            "PasswordManager - Client",
            f"Do you want to delete entry '{item.entry_name}'?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No
        )
        if btn == QMessageBox.StandardButton.No:
            return
        
        func = partial(database.entries.delete_entry_by_id, item.entry_id)
        make_worker_thread(func, self.model_delete_password_entry, self.pw_parent.worker_exc_received)

        self.entries_model.delete_entry(index)
        self.ui.passwordEntriesTableView.clearSelection()

        logger.info("Deleting entry '%s'", item.entry_name)
    
    @Slot()
    def model_delete_password_entry(self, success: bool):
        self.ui.statusbar.showMessage("Entry successfully deleted")


class PasswordGroupsItemController(QObject):
    groupChanged = Signal(GroupParentData)

    def __init__(self, pw_parent: PasswordsTabController):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui
        self.worker_exc_received = pw_parent.worker_exc_received

        self.groups_model = QStandardItemModel(parent=self)
        self.current_group: GroupParentData = None

        # TODO: Refactor this if needed
        self.root_item: QStandardItem = None
        self._items: dict[uuid.UUID, QStandardItem] = {}

        self.setup()

    def setup(self):
        self.ui.passwordGroupsTreeView.setModel(self.groups_model)

        self.ui.passwordGroupsTreeView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.passwordGroupsTreeView.customContextMenuRequested.connect(self.context_menu_event)

        self.ui.passwordGroupsTreeView.clicked.connect(self.treeview_clicked)
        self.ui.passwordGroupsTreeView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        header = self.ui.passwordGroupsTreeView.header()
        header.setStretchLastSection(True)

        header.setTextElideMode(Qt.TextElideMode.ElideNone)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)

        # Auto show the horizontal scrollbar when updating the model
        tree = self.ui.passwordGroupsTreeView

        tree.expanded.connect(lambda idx: tree.resizeColumnToContents(idx.column()))
        tree.collapsed.connect(lambda idx: tree.resizeColumnToContents(idx.column()))

        m = tree.model()
        for sig in (m.rowsInserted, m.rowsRemoved, m.modelReset, m.dataChanged):
            sig.connect(lambda *args: tree.resizeColumnToContents(0))

        self.ui.passwordGroupsTreeView.expandAll()
        self.ui.passwordGroupsTreeView.resizeColumnToContents(0)

        make_worker_thread(
            database.groups.get_children_of_root, self.after_get_root_group,
            self.worker_exc_received
        )

    @Slot()
    def after_get_root_group(self, root_group: GroupParentData):
        parentItem = self.groups_model.invisibleRootItem()

        self.root_item = QStandardItem("Root")
        self.root_item.setEditable(False)

        self.root_item.setData(root_group, Qt.ItemDataRole.UserRole)
        parentItem.appendRow(self.root_item)

        self._items[root_group.group_id] = self.root_item

        self.groups_model.setHeaderData(0, Qt.Orientation.Horizontal, "Groups")
        self.load_groups(root_group, parent_item=None)

        self.current_group = root_group
        self.groupChanged.emit(root_group)
    
    def load_groups(self, parent_group: GroupParentData, parent_item: QStandardItem | None = None):
        """Queries the database, use this in a worker thread."""
        children = database.groups.get_children_of_group(parent_group.group_id)
        parentItem = parent_item or self.root_item

        for group in children.child_groups:
            item = self.append_group(group, parentItem)
            self._items[group.group_id] = item

            logger.info(
                "Got child group [%s - %s] of group '%s'", group.group_id, 
                group.group_name, parent_group.group_name
            )
            self.load_groups(group, parent_item=item)
    
    def append_group(
            self, group: GroupParentData, 
            parent_item: QStandardItem | None = None
    ) -> QStandardItem:
        parentItem = parent_item or self.root_item

        item = QStandardItem(f"{group.group_name}")
        item.setEditable(False)

        item.setData(group, role=Qt.ItemDataRole.UserRole)
        parentItem.appendRow(item)

        logger.info(
            "Appended group [%s - %s] to tree model",
            group.group_id, group.group_name,
        )
        return item
    
    @Slot()
    def treeview_clicked(self, index: QModelIndex):
        data: GroupParentData = index.data(Qt.ItemDataRole.UserRole)
        self.current_group = data
        
        self.groupChanged.emit(data)

    @Slot()
    def context_menu_event(self, pos):
        context = QMenu(self.mw_parent)

        # Icons
        list_add_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        list_remove_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))

        # Actions
        add_group_action = QAction("Add group", self, icon=list_add_icon)
        remove_group_action = QAction("Remove group", self, icon=list_remove_icon)

        # Triggers
        add_group_action.triggered.connect(self.add_password_group)
        context.addAction(add_group_action)

        # Item-dependent triggers
        indexes = self.ui.passwordGroupsTreeView.selectedIndexes()
        if indexes:
            index = indexes[0]
            current_item: PasswordEntryData = self.groups_model.data(index, Qt.ItemDataRole.UserRole)

            remove_group_action.triggered.connect(lambda: self.delete_password_group(index, current_item))

        # Item-dependent actions
        if indexes:
            context.addAction(remove_group_action)
        
        context.exec(self.ui.passwordGroupsTreeView.mapToGlobal(pos))
    
    @Slot()
    def add_password_group(self):
        dialog = AddPasswordGroupDialog(self)

        @Slot(AddPasswordGroup)
        def dialog_accepted(data: AddPasswordGroup):
            func = partial(
                database.groups.create_group,
                data.group_name, self.current_group.group_id
            )
            make_worker_thread(func, self.add_password_group_complete, self.worker_exc_received)
        
        dialog.dataComplete.connect(dialog_accepted)
        dialog.exec()

        dialog.deleteLater()
    
    @Slot()
    def add_password_group_complete(self, data: GroupParentData):
        item = self._items[data.parent_id]
        new_item = self.append_group(data, item)

        self._items[data.group_id] = new_item

    def delete_password_group(self, index: QModelIndex, data: GroupParentData):
        root_data: GroupParentData = self.root_item.data(Qt.ItemDataRole.UserRole)
        if root_data.group_id == data.group_id:
            QMessageBox.warning(
                self.mw_parent,
                "PasswordManager - Client",
                "This group is the top-level group, you cannot delete it.",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok
            )
            return
        
        btn = QMessageBox.information(
            self.mw_parent,
            "PasswordManager - Client",
            f"Do you want to delete group '{data.group_name}'? This will remove all entries in that group.",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No
        )
        if btn == QMessageBox.StandardButton.No:
            return
        
        func = partial(
            database.groups.delete_group,
            data.group_id
        )

        @Slot()
        def delete_complete():
            parent_index = index.parent()
            if parent_index.isValid():
                parent_item = self.groups_model.itemFromIndex(parent_index) 
            else:
                parent_item = self.groups_model.invisibleRootItem()

            row = index.row()
            items = parent_item.takeRow(row)

            for item in items:
                if item is None:
                    continue

                group = item.data(Qt.ItemDataRole.UserRole)
                del self._items[group.group_id]

            self.ui.passwordGroupsTreeView.clearSelection()
        
        make_worker_thread(func, delete_complete, self.worker_exc_received)


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


# TODO: Add metadata like description, etc
class AddPasswordGroupDialog(QDialog):
    dataComplete = Signal(AddPasswordGroup)
    def __init__(self, /, parent: PasswordGroupsItemController):
        super().__init__(parent.mw_parent)
        self.ui = Ui_AddPasswordGroupDialog()
        
        self.pw_parent = parent
        self.ui.setupUi(self)
    
    def accept(self):
        group_name = self.ui.groupNameLineEdit.text()
        data = AddPasswordGroup(
            group_name=group_name
        )

        self.dataComplete.emit(data)
        return super().accept()
