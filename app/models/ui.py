import logging
import typing
import uuid
from datetime import datetime
from pathlib import Path

from pydantic import AnyUrl
from PySide6.QtCore import QAbstractListModel, QAbstractTableModel, QAbstractItemModel, QModelIndex, Qt

from .models import GroupChildrenData, GroupParentData, PasswordEntryData

if typing.TYPE_CHECKING:
    from ..controllers.tabs.databases import DatabasesTabController
    from ..controllers.tabs.passwords import PasswordEntriesController

logger: logging.Logger = logging.getLogger("passwordmanager-client")


class PasswordEntriesTableModel(QAbstractTableModel):
    def __init__(self, /, parent: "PasswordEntriesController" = None):
        super().__init__(parent)
        self.pw_ctrl = parent

        self._display_data: list[list[str | datetime]] = []
        self._item_data: list[PasswordEntryData] = []

        self._idx_lookup: dict[uuid.UUID, int] = {}
        self._col_headers: list[str] = ["Title", "Username", "URL", "Created At"]

    def rowCount(self, /, parent: QModelIndex = None):
        return len(self._item_data)

    def columnCount(self, /, parent: QModelIndex = None):
        return len(self._col_headers)

    def data(self, index, /, role):
        if role == Qt.ItemDataRole.UserRole:
            return self._item_data[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._display_data[index.row()][index.column()]
            if isinstance(value, datetime):
                return value.strftime("%x %X")

            if isinstance(value, AnyUrl):
                return str(value)

            if value is None:
                logger.debug("Received 'None' value at cell [%d, %d]", index.row(), index.column())
                return ""

            return value

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

        self._idx_lookup.clear()
        logger.debug("Cleared all password entries")

        for entry in entries:
            display_data = [entry.title, entry.username, entry.url, entry.created_at]
            self._display_data.append(display_data)

            self._item_data.append(entry)
            self._idx_lookup[entry.entry_id] = self._item_data.index(entry)

        logger.debug("Added %d entries to password entry model", len(self._item_data))
        self.endResetModel()

    def add_entry(self, entry: PasswordEntryData):
        display_data = [entry.title, entry.username, entry.url, entry.created_at]

        self._item_data.append(entry)
        self._display_data.append(display_data)

        self._idx_lookup[entry.entry_id] = self._item_data.index(entry)
        self.layoutChanged.emit()

    def delete_entry(self, data: PasswordEntryData):
        row = self._idx_lookup.get(data.entry_id, None)
        if row is None:
            logger.warning("Entry ID '%s' not in model", data.entry_id)
            return

        del self._item_data[row]
        del self._display_data[row]

        del self._idx_lookup[data.entry_id]
        self.layoutChanged.emit()

    def update_entry(self, data: PasswordEntryData):
        row = self._idx_lookup.get(data.entry_id, None)
        if row is None:
            logger.warning("Entry ID '%s' not in model", data.entry_id)
            return

        display_data = [data.title, data.username, data.url, data.created_at]

        self._item_data[row] = data
        self._display_data[row] = display_data

        top = self.index(row, 0)
        bottom = self.index(row, self.columnCount() - 1)

        self.dataChanged.emit(top, bottom)


class RecentDatabasesListModel(QAbstractListModel):
    def __init__(self, /, parent: "DatabasesTabController" = None):
        super().__init__(parent)
        self.db_ctrl = parent

        self._display_data: list[str] = []
        self._item_data: list[Path] = []

    def rowCount(self, /, parent: QModelIndex = None):
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


class PasswordGroupItem:
    def __init__(
        self, data: GroupParentData | None, parent: typing.Optional["PasswordGroupItem"] = None, root: bool = False
    ):
        self.parent_item = parent
        self.child_items = []

        self._invis_root: bool = root

        self._item_data: GroupParentData = data
        self._display_data: list = [data.group_name] if data else None

    def append_child(self, item: "PasswordGroupItem"):
        self.child_items.append(item)

    def child(self, row: int):
        return self.child_items[row]

    def child_count(self):
        return len(self.child_items)

    def display_data(self, column: int):
        if self._invis_root:
            raise ValueError("Cannot get display data of invisible root item")

        return self._display_data[column]

    def data(self):
        if self._invis_root:
            raise ValueError("Cannot get display data of invisible root item")

        return self._item_data

    def parent(self):
        return self.parent_item

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0


class PasswordGroupsTreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._invis_root_item = PasswordGroupItem(None, parent=None, root=True)
        self._col_headers: list[str] = ["Groups"]

        self._items_by_id: dict[uuid.UUID, PasswordGroupItem] = {}

    def rowCount(self, parent):
        if not parent.isValid():
            parent_item = self._invis_root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()

    def columnCount(self, parent):
        return len(self._col_headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.UserRole):
        if not index.isValid():
            return None

        item: PasswordGroupItem = index.internalPointer()
        if role == Qt.ItemDataRole.UserRole:
            return item.data()

        if role == Qt.ItemDataRole.DisplayRole:
            return item.display_data(index.column())

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._col_headers[section]

        return super().headerData(section, orientation, role)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item: PasswordGroupItem = index.internalPointer()
        parent_item: PasswordGroupItem = child_item.parent()

        if parent_item == self._invis_root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._invis_root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def add_root_group(self, group: GroupParentData):
        item = PasswordGroupItem(group, parent=self._invis_root_item)
        self._invis_root_item.append_child(item)

        self._items_by_id[group.group_id] = item
        self.layoutChanged.emit()

    def add_group(self, group: GroupParentData | GroupChildrenData):
        parent_item = self.item_by_id(group.parent_id)
        if not parent_item:
            logger.warning("Invalid parent group ID '%s'", group.parent_id)
            logger.warning("%s", group.model_dump_json(indent=4))
            return

        if not self._items_by_id.get(group.group_id):
            item = PasswordGroupItem(group, parent=parent_item)
            parent_item.append_child(item)

            self._items_by_id[group.group_id] = item
            logger.debug("Added group ID '%s' to model", group.group_id)
        else:
            logger.debug("Group ID '%s' already exists, not duplicating", group.group_id)

        self.layoutChanged.emit()

    def remove_group(self, group: GroupParentData):
        parent_item = self.item_by_id(group.parent_id)
        item = self.item_by_id(group.group_id)

        if not parent_item:
            logger.warning("Invalid parent group ID '%s'", group.parent_id)
            return False

        row = parent_item.child_items.index(item)
        parent_index = self.createIndex(parent_item.row(), 0, parent_item)

        self.beginRemoveRows(parent_index, row, row)
        parent_item.child_items.pop(row)

        self.endRemoveRows()
        return True

    def item_by_id(self, group_id: uuid.UUID) -> PasswordGroupItem | None:
        return self._items_by_id.get(group_id, None)
