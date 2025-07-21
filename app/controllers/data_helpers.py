import logging
import typing
from abc import ABCMeta, abstractmethod
from functools import partial

from PySide6.QtCore import QObject, Signal, Slot
from pydantic import TypeAdapter

from ..localdb.database import MainDatabase
from ..models.models import (
    AddPasswordGroup,
    EditedEntryWithID,
    EditedPasswordEntryInfo,
    GroupChildrenData,
    GroupParentData,
    PasswordEntryData,
)
from ..serversync.client import SyncClient
from ..serversync.models import EntryPublicGet, GroupPublicGet
from ..workers import make_worker_thread

if typing.TYPE_CHECKING:
    from .tabs.passwords import PasswordEntriesController


# TODO: Add better logging and error handling
logger: logging.Logger = logging.getLogger("passwordmanager-client")


# TODO: Add functionality to sync data created while sync was disabled
class EntriesDataController(QObject):
    def __init__(self, parent: "PasswordEntriesController"):
        super().__init__(parent)

        self.mw_parent = parent.mw_parent
        self.ctrl_parent = parent

        self.ui = self.mw_parent.ui

        self.db: MainDatabase = parent.db
        self.client: SyncClient = parent.client

        self.worker_exc_received = self.ctrl_parent.pw_parent.worker_exc_received

        # Helpers
        self.add_entry = AddEntryHelper(self)
        self.delete_entry = DeleteEntryHelper(self)

        self.update_entry = UpdateEntryHelper(self)
        self.fetch_entries = FetchEntriesHelper(self)


class GroupsDataController(QObject):
    def __init__(self, parent: "PasswordEntriesController"):
        super().__init__(parent)

        self.mw_parent = parent.mw_parent
        self.ctrl_parent = parent

        self.ui = self.mw_parent.ui

        self.db: MainDatabase = parent.db
        self.client: SyncClient = parent.client

        self.worker_exc_received = self.ctrl_parent.pw_parent.worker_exc_received

        # Helpers
        self.add_group = AddGroupHelper(self)
        self.delete_group = DeleteGroupHelper(self)

        self.fetch_root = FetchRootGroupHelper(self)
        self.fetch_children = FetchGroupChildrenHelper(self)


class MetaQObjectABC(type(QObject), ABCMeta):
    pass


class BaseHelper(QObject, metaclass=MetaQObjectABC):
    """Base class for data helpers."""

    def __init__(self, parent: EntriesDataController):
        super().__init__(parent)

        self.mw_parent = parent.mw_parent
        self.ui = self.mw_parent.ui

        self.db: MainDatabase = parent.db
        self.client: SyncClient = parent.client

    @abstractmethod
    def start_processing(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_server_call(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_db_call(self, *args, **kwargs):
        pass

    @abstractmethod
    def db_call_failed(self, exc: Exception):
        pass

    @abstractmethod
    def server_call_failed(self, exc: Exception):
        pass


class AddEntryHelper(BaseHelper):
    addEntryComplete = Signal(PasswordEntryData)

    def __init__(self, parent):
        super().__init__(parent)

    @Slot(EditedPasswordEntryInfo)
    def start_processing(self, data: EditedPasswordEntryInfo):
        if self.client.enabled:
            net_func = partial(self.client.entries.create_entry, data.group_id, data)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)

            logger.info("Sent request to add password entry")
            return

        func = partial(self.db.entries.create_entry, data.group_id, data)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

        logger.debug("Client disabled, adding entry '%s' to local database", data.title)

    @Slot(EntryPublicGet)
    def after_server_call(self, entry: EntryPublicGet):
        url_or_none = entry.url.model_dump() if entry.url is not None else None

        data = EditedPasswordEntryInfo(
            title=entry.title,
            username=entry.username,
            password=entry.password,
            url=url_or_none,
            notes=entry.notes,
            group_id=entry.group_id,
        )
        func = partial(
            self.db.entries.create_entry, entry.group_id, data, entry_id=entry.entry_id, created_at=entry.created_at
        )
        make_worker_thread(func, self.after_db_call, self.db_call_failed)
        logger.debug("Server response OK, adding entry '%s' to local database", entry.title)

    @Slot(PasswordEntryData)
    def after_db_call(self, entry: PasswordEntryData):
        logger.debug("Entry '%s' added to database", entry.title)
        self.addEntryComplete.emit(entry)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class DeleteEntryHelper(BaseHelper):
    deleteEntryComplete = Signal(PasswordEntryData)

    def __init__(self, parent: EntriesDataController):
        super().__init__(parent)

    def _net_delete(self, data: PasswordEntryData):
        if not self.client.enabled:
            raise RuntimeError("Called _net_delete with a disabled client")

        self.client.entries.delete_entry_by_id(data.entry_id, data.group_id)
        return data

    def _db_delete(self, data: PasswordEntryData):
        self.db.entries.delete_entry_by_id(data.entry_id, data.group_id)
        return data

    def start_processing(self, data: PasswordEntryData):
        if self.client.enabled:
            net_func = partial(self._net_delete, data)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)
            return

        func = partial(self._db_delete, data)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

        logger.debug("Client disabled, deleting entry '%s'", data.title)

    @Slot(EntryPublicGet)
    def after_server_call(self, data: PasswordEntryData):
        func = partial(self._db_delete, data)

        make_worker_thread(func, self.after_db_call, self.db_call_failed)
        logger.debug("Server response OK, deleting entry '%s' from local database", data.title)

    @Slot(PasswordEntryData)
    def after_db_call(self, entry: PasswordEntryData):
        logger.debug("Entry '%s' deleted from database", entry.title)
        self.deleteEntryComplete.emit(entry)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class UpdateEntryHelper(BaseHelper):
    updateEntryComplete = Signal(PasswordEntryData)

    def __init__(self, parent):
        super().__init__(parent)

    @Slot(EditedEntryWithID)
    def start_processing(self, data: EditedEntryWithID):
        if self.client:
            net_func = partial(self.client.entries.update_entry_data, data.entry_id, data)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)

            logger.info("Sending request to edit entry...")
            return

        func = partial(self.db.entries.update_entry_data, data.entry_id, data)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

    @Slot(EntryPublicGet)
    def after_server_call(self, data: EntryPublicGet):
        # This is used because it's a RootModel generated instead of an actual AnyUrl
        url_or_none = data.url.model_dump() if data.url is not None else None

        entry = EditedEntryWithID(
            title=data.title,
            username=data.username,
            password=data.password,
            url=url_or_none,
            notes=data.notes,
            entry_id=data.entry_id,
            group_id=data.group_id,
        )
        func = partial(self.db.entries.update_entry_data, data.entry_id, entry)

        make_worker_thread(func, self.after_db_call, self.db_call_failed)
        logger.debug("Server response OK, updating entry '%s'", data.title)

    @Slot(PasswordEntryData)
    def after_db_call(self, data: PasswordEntryData):
        logger.debug("Entry '%s' updated", data.title)
        self.updateEntryComplete.emit(data)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class FetchEntriesHelper(BaseHelper):
    fetchEntriesComplete = Signal(list)

    def __init__(self, parent):
        super().__init__(parent)

    def _process_entries(self, group: GroupParentData):
        if self.client.enabled:
            net_entries = self.client.entries.get_entries_by_group(group.group_id, amount=100, offset=0)
        else:
            net_entries = None

        db_entries = self.db.entries.get_entries_by_group(group.group_id, amount=100, offset=0)
        if net_entries is None:
            logger.debug("Client disabled, returning entries found in database")
            return db_entries

        len_net_entries = len(net_entries)
        len_db_entries = len(db_entries)

        if len_net_entries != len_db_entries:
            logger.error(
                "Retrieved %d entries from server, only retrieved %d entries from local database",
                len_net_entries,
                len_db_entries,
            )
            raise RuntimeError(f"expected {len_net_entries} entries from client, only got {len_db_entries}")

        conv_entries: list[PasswordEntryData] = []
        for entry in net_entries:
            url_or_none = entry.url.model_dump() if entry.url is not None else None
            conv_entry = PasswordEntryData(
                title=entry.title,
                username=entry.username,
                password=entry.password,
                url=url_or_none,
                notes=entry.notes,
                entry_id=entry.entry_id,
                group_id=entry.group_id,
                created_at=entry.created_at,
            )
            conv_entries.append(conv_entry)

        return conv_entries

    def start_processing(self, group: GroupParentData):
        # TODO: Implement paging using the amount and offset
        if self.client.enabled:
            net_func = partial(self._process_entries, group)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)
            return

        func = partial(self._process_entries, group)

        make_worker_thread(func, self.after_db_call, self.db_call_failed)
        logger.info("Reloading entries for group '%s'", group.group_name)

    @Slot(list)
    def after_server_call(self, entries: list[PasswordEntryData]):
        self.fetchEntriesComplete.emit(entries)

    @Slot(list)
    def after_db_call(self, entries: list[PasswordEntryData]):
        self.fetchEntriesComplete.emit(entries)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class AddGroupHelper(BaseHelper):
    addGroupComplete = Signal(GroupParentData)

    def __init__(self, parent):
        super().__init__(parent)

    @Slot(AddPasswordGroup)
    def start_processing(self, data: AddPasswordGroup):
        if self.client.enabled:
            net_func = partial(self.client.groups.create_group, data.group_name, parent_id=data.parent_id)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)

            logger.info("Sent request to add password group")
            return

        func = partial(self.db.groups.create_group, data.group_name, parent_id=data.parent_id)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

    @Slot(GroupPublicGet)
    def after_server_call(self, group: GroupPublicGet):
        func = partial(
            self.db.groups.create_group, group.group_name, parent_id=group.parent_id, group_id=group.group_id
        )
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

    @Slot(GroupParentData)
    def after_db_call(self, group: GroupParentData):
        logger.debug("Group '%s' added to database", group.group_name)
        self.addGroupComplete.emit(group)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class DeleteGroupHelper(BaseHelper):
    deleteGroupComplete = Signal(GroupParentData)

    def __init__(self, parent: EntriesDataController):
        super().__init__(parent)

    def _net_delete(self, data: GroupParentData):
        if not self.client.enabled:
            raise RuntimeError("Called _net_delete with a disabled client")

        self.client.groups.delete_group(data.group_id)
        return data

    def _db_delete(self, data: GroupParentData):
        self.db.groups.delete_group(data.group_id)
        return data

    def start_processing(self, data: GroupParentData):
        if self.client.enabled:
            net_func = partial(self._net_delete, data)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)
            return

        func = partial(self._db_delete, data)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

        logger.debug("Client disabled, deleting group '%s'", data.group_name)

    @Slot(EntryPublicGet)
    def after_server_call(self, data: GroupParentData):
        func = partial(self._db_delete, data)

        make_worker_thread(func, self.after_db_call, self.db_call_failed)
        logger.debug("Server response OK, deleting group '%s' from local database", data.group_name)

    @Slot(PasswordEntryData)
    def after_db_call(self, group: GroupParentData):
        logger.debug("Group '%s' deleted from database", group.group_name)
        self.deleteGroupComplete.emit(group)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class FetchRootGroupHelper(BaseHelper):
    fetchRootComplete = Signal(GroupParentData)

    def __init__(self, parent):
        super().__init__(parent)

    def _process_root(self):
        if self.client.enabled:
            net_group = self.client.groups.get_root_info()
        else:
            net_group = None
        
        db_group = self.db.groups.get_root_info()
        if net_group is None:
            logger.debug("Client disabled, returning group found in database")
            return db_group

        conv_group = GroupParentData.model_validate(net_group, from_attributes=True)
        if db_group != conv_group:
            logger.error(
                "Local group [ID: %s] '%s' does not match remote group [ID: %s] '%s'",
                db_group.group_id, db_group.group_name, conv_group.group_id, conv_group.group_name
            )
            raise RuntimeError(f"local group {db_group.group_name} does not match remote group {conv_group.group_name}")

        return conv_group
    
    def start_processing(self):
        if self.client.enabled:
            make_worker_thread(self._process_root, self.after_server_call, self.server_call_failed)
            return

        make_worker_thread(self._process_root, self.after_db_call, self.db_call_failed)

    @Slot(tuple)
    def after_server_call(self, data: GroupParentData):
        self.fetchRootComplete.emit(data)

    @Slot(tuple)
    def after_db_call(self, data: GroupParentData):
        self.fetchRootComplete.emit(data)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)


class FetchGroupChildrenHelper(BaseHelper):
    fetchRootChildrenComplete = Signal(list)
    fetchGroupChildrenComplete = Signal(list)

    def __init__(self, parent):
        super().__init__(parent)

    def _process_groups(self, group: GroupParentData | None):
        if self.client.enabled:
            if group is None:
                net_groups = self.client.groups.get_children_of_root()
            else:
                net_groups = self.client.groups.get_children_of_group(group.group_id)
        else:
            net_groups = None
        
        if group is None:
            db_groups = self.db.groups.get_children_of_root()
        else:
            db_groups = self.db.groups.get_children_of_group(group.group_id)
        
        if net_groups is None:
            logger.debug("Client disabled, returning groups found in database")
            return db_groups

        ta = TypeAdapter(list[GroupChildrenData])
        conv_group = ta.validate_python(net_groups, from_attributes=True)

        if db_groups != conv_group:
            logger.error(
                "Local group mismatch",
            )
            raise RuntimeError("mismatch")

        return (conv_group, True if group is None else False)
    
    def process_threadless(self, group: GroupParentData | None):
        return self._process_groups(group)

    def start_processing(self, group: GroupParentData | None):
        func = partial(self._process_groups, group)
        if self.client.enabled:
            make_worker_thread(func, self.after_server_call, self.server_call_failed)
            return

        make_worker_thread(func, self.after_db_call, self.db_call_failed)

    @Slot(tuple)
    def after_server_call(self, data: tuple[list, bool]):
        groups, was_root = data
        if was_root:
            self.fetchRootChildrenComplete.emit(groups)
        else:
            self.fetchGroupChildrenComplete.emit(groups)

    @Slot(tuple)
    def after_db_call(self, data: tuple[list, bool]):
        groups, was_root = data
        if was_root:
            self.fetchRootChildrenComplete.emit(groups)
        else:
            self.fetchGroupChildrenComplete.emit(groups)

    @Slot(Exception)
    def db_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)

    @Slot(Exception)
    def server_call_failed(self, exc: Exception):
        logger.error("Error:", exc_info=exc)
