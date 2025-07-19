import logging
import typing
from abc import ABCMeta, abstractmethod
from functools import partial

from PySide6.QtCore import QObject, Signal, Slot

from ..localdb.database import MainDatabase
from ..models.models import (
    EditedEntryWithGroup,
    EditedPasswordEntryInfo,
    GroupParentData,
    PasswordEntryData,
)
from ..serversync.client import SyncClient
from ..serversync.models import EntryPublicGet
from ..workers import make_worker_thread

if typing.TYPE_CHECKING:
    from .tabs.passwords import PasswordEntriesController


logger: logging.Logger = logging.getLogger("passwordmanager-client")


# TODO: Refactor to make it so that istead of storing all CRUD opts in one class,
# its split into many classes with either add, delete, edit or read
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

    def group_changed(self, group: GroupParentData):
        self.add_entry.group_changed(group)
        func = partial(self.db.entries.get_entries_by_group, group.group_id)

        make_worker_thread(func, self.entries_reloaded, self.worker_exc_received)
        logger.info("Reloading entries for group '%s'", group.group_name)

    @Slot(list)
    def entries_reloaded(self, entries: list[PasswordEntryData]):
        self.entriesReloaded.emit(entries)


class MetaQObjectABC(type(QObject), ABCMeta):
    pass


class BaseEntryHelper(QObject, metaclass=MetaQObjectABC):
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


class AddEntryHelper(BaseEntryHelper):
    addEntryComplete = Signal(PasswordEntryData)

    def __init__(self, parent):
        super().__init__(parent)
        self.current_group: GroupParentData = None

    def group_changed(self, group: GroupParentData):
        self.current_group = group

    @Slot(EditedPasswordEntryInfo)
    def start_processing(self, data: EditedPasswordEntryInfo):
        if self.client.enabled:
            net_func = partial(self.client.entries.create_entry, self.current_group.group_id, data)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)

            logger.info("Sent request to add password entry")
            return

        func = partial(self.db.entries.create_entry, self.current_group.group_id, data)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

        logger.debug("Client disabled, adding entry '%s' to local database", data.title)

    @Slot(EntryPublicGet)
    def after_server_call(self, entry: EntryPublicGet):
        url_or_none = entry.url.model_dump() if entry.url is not None else None

        data = EditedPasswordEntryInfo(
            title=entry.title, username=entry.username, password=entry.password, url=url_or_none, notes=entry.notes
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


class DeleteEntryHelper(BaseEntryHelper):
    deleteEntryComplete = Signal(PasswordEntryData)

    def __init__(self, parent: EntriesDataController):
        super().__init__(parent)

    def _process_delete(self, data: PasswordEntryData):
        if self.client.enabled:
            self.client.entries.delete_entry_by_id(data.entry_id, data.group_id)
        else:
            self.db.entries.delete_entry_by_id(data.entry_id, data.group_id)

        return data

    def start_processing(self, data: PasswordEntryData):
        if self.client.enabled:
            net_func = partial(self._process_delete, data)
            make_worker_thread(net_func, self.after_server_call, self.server_call_failed)
            return

        func = partial(self._process_delete, data)
        make_worker_thread(func, self.after_db_call, self.db_call_failed)

        logger.debug("Client disabled, deleting entry '%s'", data.title)

    @Slot(EntryPublicGet)
    def after_server_call(self, data: PasswordEntryData):
        func = partial(self.db.entries.delete_entry_by_id, data.entry_id, data.group_id)

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


class UpdateEntryHelper(BaseEntryHelper):
    updateEntryComplete = Signal(PasswordEntryData)

    def __init__(self, parent):
        super().__init__(parent)

    @Slot(EditedEntryWithGroup)
    def start_processing(self, data: EditedEntryWithGroup):
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

        entry = EditedEntryWithGroup(
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


class FetchEntriesHelper(BaseEntryHelper):
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
