import logging
import traceback
import typing
import uuid
from enum import StrEnum
from functools import partial

from pydantic import AnyUrl, TypeAdapter, ValidationError
from PySide6.QtCore import QModelIndex, QObject, Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QHeaderView, QMenu, QMessageBox

from ...localdb.database import MainDatabase
from ...models.models import (
    AddPasswordGroup,
    EditedEntryWithGroup,
    EditedPasswordEntryInfo,
    GroupParentData,
    PasswordEntryData,
)
from ...models.ui import PasswordEntriesTableModel
from ...serversync.client import SyncClient
from ...serversync.models import GenericSuccess, GroupPublicModify
from ...ui.add_password_group_dialog import Ui_AddPasswordGroupDialog
from ...ui.password_entry_info_dialog import Ui_PasswordEntryInfoDialog
from ..entry_data import EntriesDataController
from ...workers import make_worker_thread

if typing.TYPE_CHECKING:
    from ..apps import AppsController


# TODO: Cleanup this module and make it readable
logger: logging.Logger = logging.getLogger("passwordmanager-client")


class EmitDialogInfoAs(StrEnum):
    add = "add"
    edit = "edit"


class PasswordsTabController(QObject):
    useClient = Signal(SyncClient)

    def __init__(self, app_parent: "AppsController"):
        super().__init__(app_parent)

        self.mw_parent = app_parent.mw_parent
        self.app_parent = app_parent

        self.ui = self.mw_parent.ui
        self.db: MainDatabase = None

        self.client: SyncClient = None

    @Slot(MainDatabase)
    def database_loaded(self, database: MainDatabase):
        self.db = database
        logger.debug("Local database loaded, waiting for client")

    @Slot(SyncClient)
    def client_loaded(self, client: SyncClient):
        if not self.db:
            raise RuntimeError("client loaded before database")

        self.client = client
        logger.debug("Client loaded, setting up controllers")

        self.setup()

    def setup(self):
        # Controllers
        self.groups_ctrl = PasswordGroupsItemController(self, self.db, self.client)
        self.entries_ctrl = PasswordEntriesController(self, self.db, self.client)

        self.entry_info_ctrl = PasswordEntryInfoController(self)
        self.groups_ctrl.groupChanged.connect(self.entries_ctrl.reload_entries)

        self.entries_ctrl.entryChanged.connect(self.entry_info_ctrl.entry_changed)

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
        logger.error("Exception when running worker:", exc_info=exc)


# TODO: Keep track of data created while server sync is disabled to make it easier to sync
class PasswordEntriesController(QObject):
    entryChanged = Signal(PasswordEntryData)

    def __init__(self, pw_parent: PasswordsTabController, database: MainDatabase, client: SyncClient):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui

        self.db: MainDatabase = database
        self.client: SyncClient = client

        self.entries_model = PasswordEntriesTableModel(parent=self)
        self.ui.passwordEntriesTableView.setModel(self.entries_model)

        self.entry_info_dialog = PasswordEntryInfoDialog(self)
        self.data_ctrl: EntriesDataController = EntriesDataController(self)

        self.setup()

    def setup(self):
        header = self.ui.passwordEntriesTableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        header.setStretchLastSection(True)

        self.ui.passwordEntriesTableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.passwordEntriesTableView.customContextMenuRequested.connect(self.context_menu_event)

        self.ui.passwordEntriesTableView.clicked.connect(self.tableview_clicked)
        self.ui.passwordEntriesTableView.doubleClicked.connect(self.tableview_doubleclicked)

        self.entry_info_dialog.addEntryRequested.connect(self.data_ctrl.add_entry.start_processing)
        self.entry_info_dialog.editEntryRequested.connect(self.data_ctrl.update_entry.start_processing)

        self.data_ctrl.add_entry.addEntryComplete.connect(self.model_add_password_entry)
        self.data_ctrl.delete_entry.deleteEntryComplete.connect(self.model_delete_password_entry)

        self.data_ctrl.update_entry.updateEntryComplete.connect(self.model_edit_password_entry)
        self.data_ctrl.fetch_entries.fetchEntriesComplete.connect(self.model_reload_entries)

    @Slot()
    def context_menu_event(self, pos):
        context = QMenu(self.mw_parent)

        # Icons
        list_add_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        list_remove_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))

        doc_props_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))

        # Actions
        add_entry_action = QAction("Add entry", self, icon=list_add_icon)
        remove_entry_action = QAction("Remove entry", self, icon=list_remove_icon)

        edit_entry_action = QAction("Edit entry", self, icon=doc_props_icon)

        # Triggers
        add_entry_action.triggered.connect(self.add_password_entry)
        context.addAction(add_entry_action)

        # Item-dependent triggers
        indexes = self.ui.passwordEntriesTableView.selectedIndexes()
        if indexes:
            # Get only the first index, because the QTableView uses the SelectRows behavior
            index = indexes[0]
            current_item: PasswordEntryData = self.entries_model.data(index, Qt.ItemDataRole.UserRole)

            remove_entry_action.triggered.connect(lambda: self.delete_password_entry(current_item))
            edit_entry_action.triggered.connect(lambda: self.edit_password_entry(current_item))

        # Item-dependent actions
        if indexes:
            context.addAction(remove_entry_action)
            context.addAction(edit_entry_action)

        context.exec(self.ui.passwordEntriesTableView.mapToGlobal(pos))

    @Slot(QModelIndex)
    def tableview_clicked(self, index: QModelIndex):
        data: PasswordEntryData = index.data(Qt.ItemDataRole.UserRole)
        self.entryChanged.emit(data)

    @Slot(QModelIndex)
    def tableview_doubleclicked(self, index: QModelIndex):
        data: PasswordEntryData = index.data(Qt.ItemDataRole.UserRole)
        self.edit_password_entry(data)

    @Slot(GroupParentData)
    def reload_entries(self, group: GroupParentData):
        self.data_ctrl.add_entry.group_changed(group)
        self.data_ctrl.fetch_entries.start_processing(group)

        self.ui.statusbar.showMessage(f"Passwords - Reloading entries for group '{group.group_name}'", timeout=5000)

    @Slot(list)
    def model_reload_entries(self, entries: list[PasswordEntryData]):
        logger.info("Fetched %d entries", len(entries))
        self.entries_model.load_entries(entries)

        self.ui.statusbar.showMessage("Passwords - Entries reloaded", timeout=5000)

    @Slot()
    def add_password_entry(self):
        self.entry_info_dialog.reset_data(emit_as=EmitDialogInfoAs.add)
        self.entry_info_dialog.show()

    @Slot(PasswordEntryData)
    def model_add_password_entry(self, entry: PasswordEntryData):
        logger.info("Adding entry '%s'", entry.title)
        self.ui.statusbar.showMessage(f"Passwords - Adding entry '{entry.title}'", timeout=5000)

        self.entries_model.add_entry(entry)

    def delete_password_entry(self, item: PasswordEntryData):
        btn = QMessageBox.information(
            self.mw_parent,
            "PasswordManager - Client",
            f"Do you want to delete entry '{item.title}'?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No,
        )
        if btn == QMessageBox.StandardButton.No:
            return

        logger.info("Deleting entry '%s'", item.title)
        self.ui.statusbar.showMessage(f"Passwords - Deleting entry '{item.title}'", timeout=5000)

        self.data_ctrl.delete_entry.start_processing(item)

    @Slot(PasswordEntryData)
    def model_delete_password_entry(self, entry: PasswordEntryData):
        self.entries_model.delete_entry(entry)
        self.ui.passwordEntriesTableView.clearSelection()

        self.ui.statusbar.showMessage("Passwords - Entry deleted")

    def edit_password_entry(self, item: PasswordEntryData):
        self.entry_info_dialog.reset_data(emit_as=EmitDialogInfoAs.edit)
        self.entry_info_dialog.set_existing_data(item)

        self.entry_info_dialog.show()

    @Slot(PasswordEntryData)
    def model_edit_password_entry(self, entry: PasswordEntryData):
        logger.info("Updating entry '%s'", entry.title)
        self.ui.statusbar.showMessage(f"Passwords - Updating entry '{entry.title}'", timeout=5000)

        self.entries_model.update_entry(entry)

        indexes = self.ui.passwordEntriesTableView.selectedIndexes()
        if not indexes:
            logger.debug("No selected indexes")
            return

        index = indexes[0]
        if index.data(Qt.ItemDataRole.UserRole) == entry:
            logger.debug("Entry changed is the currently selected entry, updating")
            self.entryChanged.emit(entry)

        return


# TODO: Ensure when setting up sync for the first time, root group always matches the server
# TODO: Use an actual tree model instead of relying on an item model
class PasswordGroupsItemController(QObject):
    groupChanged = Signal(GroupParentData)

    def __init__(self, pw_parent: PasswordsTabController, database: MainDatabase, client: SyncClient):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui

        self.db: MainDatabase = database
        self.client: SyncClient = client

        self.worker_exc_received = pw_parent.worker_exc_received

        # Controllers here
        self.add_group_dialog = AddPasswordGroupDialog(self)
        self.groups_model = QStandardItemModel(parent=self)

        self.current_group: GroupParentData = None
        self.data_ctrl: GroupsDataController = GroupsDataController(self)

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

        self.add_group_dialog.dataComplete.connect(self.data_ctrl.add_password_group_accepted)
        self.data_ctrl.addGroupComplete.connect(self.add_password_group_complete)

        # TODO: Make this use server sync too
        make_worker_thread(self.db.groups.get_children_of_root, self.after_get_root_group, self.worker_exc_received)
        self.ui.statusbar.showMessage("Passwords - Loading top-level and child groups", timeout=5000)

    @Slot()
    def after_get_root_group(self, root_group: GroupParentData):
        parentItem = self.groups_model.invisibleRootItem()

        self.root_item = QStandardItem("Root")
        self.root_item.setEditable(False)

        self.root_item.setData(root_group, Qt.ItemDataRole.UserRole)
        parentItem.appendRow(self.root_item)

        self._items[root_group.group_id] = self.root_item
        self.groups_model.setHeaderData(0, Qt.Orientation.Horizontal, "Groups")

        func = partial(self.load_groups, root_group, parent_item=None)
        make_worker_thread(func, self.all_groups_loaded, self.worker_exc_received)

    @Slot()
    def all_groups_loaded(self):
        root_group = self.root_item.data(Qt.ItemDataRole.UserRole)
        self.current_group = root_group

        self.data_ctrl.group_changed(root_group)
        self.groupChanged.emit(root_group)

        self.ui.statusbar.showMessage("Passwords - Loaded top-level and child groups", timeout=5000)

    def load_groups(self, parent_group: GroupParentData, parent_item: QStandardItem | None = None):
        """Queries the database, use this in a worker thread."""
        if self.client.enabled:
            net_children = self.client.groups.get_children_of_group(parent_group.group_id)
            db_children = self.db.groups.get_children_of_group(parent_group.group_id)

            len_net_children = len(net_children.child_groups)
            len_db_children = len(db_children.child_groups)

            if len_net_children != len_db_children:
                logger.error("Expected %d groups locally, instead got %d groups", len_net_children, len_db_children)
                # raise ValueError("Server groups do not match local groups")

            children = GroupParentData.model_validate(net_children, from_attributes=True)
        else:
            children = self.db.groups.get_children_of_group(parent_group.group_id)

        parentItem = parent_item or self.root_item

        # TODO: Improve how this is loaded, it loads recusively and can lag
        for group in children.child_groups:
            item = self.append_group(group, parentItem)
            self._items[group.group_id] = item

            logger.debug(
                "Got child group [%s - %s] of group '%s'", group.group_id, group.group_name, parent_group.group_name
            )
            self.load_groups(group, parent_item=item)

    def append_group(self, group: GroupParentData, parent_item: QStandardItem | None = None) -> QStandardItem:
        parentItem = parent_item or self.root_item

        item = QStandardItem(f"{group.group_name}")
        item.setEditable(False)

        item.setData(group, role=Qt.ItemDataRole.UserRole)
        parentItem.appendRow(item)

        logger.debug(
            "Appended group [%s - %s] to tree model",
            group.group_id,
            group.group_name,
        )
        return item

    @Slot()
    def treeview_clicked(self, index: QModelIndex):
        data: GroupParentData = index.data(Qt.ItemDataRole.UserRole)
        self.current_group = data

        self.data_ctrl.group_changed(data)
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
        self.add_group_dialog.reset_data()
        self.add_group_dialog.show()

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
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return

        btn = QMessageBox.information(
            self.mw_parent,
            "PasswordManager - Client",
            f"Do you want to delete group '{data.group_name}'? This will remove all entries in that group.",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No,
        )
        if btn == QMessageBox.StandardButton.No:
            return

        # TODO: Clean this up and figure out a better way to cleanup groups and their children
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

        @Slot()
        def sync_delete_complete(data: GenericSuccess):
            func = partial(self.db.groups.delete_group, data.group_id)
            make_worker_thread(func, delete_complete, self.worker_exc_received)

        if self.client:
            net_func = partial(self.client.groups.delete_group, data.group_id)
            make_worker_thread(net_func, sync_delete_complete, self.worker_exc_received)
        else:
            func = partial(self.db.groups.delete_group, data.group_id)
            make_worker_thread(func, delete_complete, self.worker_exc_received)


class PasswordEntryInfoController(QObject):
    def __init__(self, pw_parent: PasswordsTabController):
        super().__init__(pw_parent)

        self.mw_parent = pw_parent.mw_parent
        self.pw_parent = pw_parent

        self.ui = self.mw_parent.ui
        self.ui.entryPasswordShowHideButton.clicked.connect(self.show_hide_clicked)

        self._entry: PasswordEntryData = None
        self._hidden: bool = True

    @Slot(PasswordEntryData)
    def entry_changed(self, entry: PasswordEntryData):
        logger.debug("Entry changed to '%s', changing info", entry.title)
        self._entry = entry

        self._hidden = True

        self.ui.entryUsernameDataLabel.setText(entry.username)
        self.ui.entryPasswordDataLabel.setText("*****")

        self.ui.entryNotesPlainTextEdit.setPlainText(entry.notes)
        self.ui.entryURLDataLabel.setText(str(entry.url) if entry.url else "")

    @Slot()
    def show_hide_clicked(self):
        if not self._entry:
            return

        if self._hidden:
            self._hidden = False
            self.ui.entryPasswordDataLabel.setText(self._entry.password)
        else:
            self._hidden = True
            self.ui.entryPasswordDataLabel.setText("*****")

        logger.debug("Hidden: %s", self._hidden)


class PasswordEntryInfoDialog(QDialog):
    addEntryRequested = Signal(EditedPasswordEntryInfo)
    editEntryRequested = Signal(EditedEntryWithGroup)

    def __init__(self, /, parent: PasswordEntriesController):
        super().__init__(parent.mw_parent)
        self.ui = Ui_PasswordEntryInfoDialog()

        self.pw_parent = parent
        self.ui.setupUi(self)

        self._emit_as: EmitDialogInfoAs = None
        self._data: PasswordEntryData | None = None

        self.ui.urlLineEdit.textEdited.connect(self.url_text_edited)

    def reset_data(self, emit_as: EmitDialogInfoAs = EmitDialogInfoAs.add):
        self._emit_as = emit_as
        self._data = None

        self.ui.titleLineEdit.setText("")
        self.ui.usernameLineEdit.setText("")

        self.ui.passwordLineEdit.setText("")
        self.ui.urlLineEdit.setText("")

        self.ui.notesPlainTextEdit.setPlainText("")

    def set_existing_data(self, data: PasswordEntryData):
        self.ui.titleLineEdit.setText(data.title)
        self.ui.usernameLineEdit.setText(data.username)

        self.ui.passwordLineEdit.setText(data.password)
        self.ui.urlLineEdit.setText(str(data.url) if data.url else "")

        self.ui.notesPlainTextEdit.setPlainText(data.notes)
        self._data = data

    def accept(self):
        title = self.ui.titleLineEdit.text()
        username = self.ui.usernameLineEdit.text()

        password = self.ui.passwordLineEdit.text()
        url = self.ui.urlLineEdit.text()

        notes = self.ui.notesPlainTextEdit.toPlainText()

        data = EditedPasswordEntryInfo(title=title, username=username, password=password, url=url or None, notes=notes)

        if self._emit_as == EmitDialogInfoAs.add:
            self.addEntryRequested.emit(data)
        elif self._emit_as == EmitDialogInfoAs.edit:
            assert self._data is not None, "Edit data is invalid"

            with_group_data = EditedEntryWithGroup(
                group_id=self._data.group_id, entry_id=self._data.entry_id, **data.model_dump()
            )
            self.editEntryRequested.emit(with_group_data)

        return super().accept()

    @Slot()
    def url_text_edited(self, text: str):
        ta = TypeAdapter(AnyUrl)
        btn = self.ui.dialogButtonBox.button(QDialogButtonBox.StandardButton.Ok)

        try:
            if text:
                ta.validate_python(text)
        except ValidationError:
            btn.setEnabled(False)
            return

        btn.setEnabled(True)


# TODO: Add metadata like description, etc
class AddPasswordGroupDialog(QDialog):
    dataComplete = Signal(AddPasswordGroup)

    def __init__(self, /, parent: PasswordGroupsItemController):
        super().__init__(parent.mw_parent)
        self.ui = Ui_AddPasswordGroupDialog()

        self.pw_parent = parent
        self.ui.setupUi(self)

        self.ui.groupNameLineEdit.textEdited.connect(self.groupname_text_edited)
        self.ui.dialogButtonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def reset_data(self):
        self.ui.groupNameLineEdit.setText("")

    def accept(self):
        group_name = self.ui.groupNameLineEdit.text()
        data = AddPasswordGroup(group_name=group_name)

        self.dataComplete.emit(data)
        return super().accept()

    @Slot()
    def groupname_text_edited(self, text: str):
        btn = self.ui.dialogButtonBox.button(QDialogButtonBox.StandardButton.Ok)

        if not text:
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)


class GroupsDataController(QObject):
    addGroupComplete = Signal(GroupParentData)
    # deleteGroupComplete = Signal(bool)

    def __init__(self, parent: PasswordEntriesController):
        super().__init__(parent)

        self.mw_parent = parent.mw_parent
        self.ctrl_parent = parent

        self.ui = self.mw_parent.ui

        self.db: MainDatabase = parent.db
        self.client: SyncClient = parent.client

        self.current_group: GroupParentData = None
        self.worker_exc_received = self.ctrl_parent.pw_parent.worker_exc_received

    def group_changed(self, group: GroupParentData):
        self.current_group = group

    @Slot()
    def add_password_group_accepted(self, data: AddPasswordGroup):
        if self.client:
            net_func = partial(self.client.groups.create_group, data.group_name, self.current_group.group_id)
            make_worker_thread(net_func, self.sync_add_password_group, self.worker_exc_received)

            logger.info("Sent request to add group")
            return

        func = partial(self.db.groups.create_group, data.group_name, parent_id=self.current_group.group_id)
        make_worker_thread(func, self.add_complete, self.worker_exc_received)

    @Slot()
    def sync_add_password_group(self, group: GroupPublicModify):
        func = partial(
            self.db.groups.create_group,
            group.group_name,
            parent_id=self.current_group.group_id,
            group_id=group.group_id,
        )
        make_worker_thread(func, self.add_complete, self.worker_exc_received)

    @Slot()
    def add_complete(self, group: GroupParentData):
        self.addGroupComplete.emit(group)
