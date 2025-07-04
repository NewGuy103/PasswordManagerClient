import logging
import uuid

import httpx

from pydantic import TypeAdapter

from .database import MainDatabase
from ..models import (
    SavedSyncInfo, GroupParentData, PasswordEntryData, EditedPasswordEntryInfo,
    EditedEntryWithGroup
)

from ..client.types import Response
from ..client import AuthenticatedClient
from ..client.api.auth import auth_test_api_auth_test_auth_get as auth_test

# groups
from ..client.api.groups import create_group_api_groups_post as api_create_group
from ..client.api.groups import retrieve_top_level_groups_api_groups_get as api_get_root_group
from ..client.api.groups import get_group_children_api_groups_group_id_children_get as api_get_group
from ..client.api.groups import delete_group_api_groups_group_id_delete as api_delete_group

# entries (under groups)
from ..client.api.groups import create_password_entry_api_groups_group_id_entries_post as api_create_entry
from ..client.api.groups import get_group_entries_api_groups_group_id_entries_get as api_get_entries
from ..client.api.groups import delete_password_entry_api_groups_group_id_entries_entry_id_delete as api_delete_entry
from ..client.api.groups import change_entry_data_api_groups_group_id_entries_entry_id_put as api_update_entry


from ..client.models import (
    UserInfoPublic, GroupCreate, GroupPublicModify, GroupPublicGet, GenericSuccess,
    EntryPublicGet, EntryCreate, EntryUpdate
)


logger: logging.Logger = logging.getLogger("passwordmanager-client")
DEFAULT_CHUNK_SIZE: int = 25 * 1024 * 1024  # 25 MiB


class SyncedDatabase:
    """Abstraction that adds server sync to the local database."""
    def __init__(self):
        self.maindb: MainDatabase = None
        self.auth_client: AuthenticatedClient = None

    def setup(self, main_db: MainDatabase, sync_info: SavedSyncInfo) -> None:
        """Sets up the database and runs first-run checks.
        
        This must be called first before using the child methods.
        """

        self.auth_client: AuthenticatedClient = AuthenticatedClient(
            str(sync_info.server_url), 
            sync_info.access_token,
            raise_on_unexpected_status=True,
            timeout=30,
            httpx_args={'event_hooks': {"request": [self.log_request], "response": [self.log_response]}}
        )
        data: Response[UserInfoPublic] = auth_test.sync_detailed(client=self.auth_client)

        if data.parsed is None:
            raise ValueError("Invalid data from server during setup")
        
        if data.parsed.username != sync_info.username:
            raise ValueError("Username from sync info does not match the server")
        
        self.maindb: MainDatabase = main_db

        self.groups = PasswordGroupMethods(self)
        self.entries = PasswordEntryMethods(self)

        self.syncinfo = main_db.syncinfo  # always offline when working with Sync Info
        return

    def log_request(self, req: httpx.Request):
        headers = dict(req.headers)
        if headers.get('authorization'):
            headers['authorization'] = '...'

        logger.debug("HTTP request sent: [%s %s] - Headers: %s", req.method, req.url, headers)

    def log_response(self, res: httpx.Response):
        req = res.request
        logger.debug(
            "HTTP response received from request [%s %s] - Status Code %d - Headers: %s",
            req.method, req.url, res.status_code, dict(res.headers)
        )

    def close(self):
        if self.maindb:
            self.maindb.close()
        
        if self.auth_client:
            self.auth_client.get_httpx_client().close()


class PasswordGroupMethods:
    def __init__(self, parent: SyncedDatabase):
        self.parent = parent
        self.maindb = parent.maindb

        self.auth_client = parent.auth_client

    def create_group(self, group_name: str, parent_id: uuid.UUID) -> GroupParentData:
        body = GroupCreate(
            group_name=group_name,
            parent_id=parent_id
        )
        data: GroupPublicModify = api_create_group.sync(client=self.auth_client, body=body)
        assert data is not None

        group_parent_data = self.maindb.groups.create_group(
            group_name, parent_id=parent_id,
            group_id=data.group_id
        )
        return group_parent_data

    def get_children_of_root(self) -> GroupParentData:
        data: GroupPublicGet = api_get_root_group.sync(client=self.auth_client)
        assert data is not None

        root_data: GroupParentData = self.maindb.groups.get_children_of_root()
        model_data: GroupParentData = GroupParentData.model_validate(data, from_attributes=True)

        if root_data != model_data:
            logger.error(
                "Local group '%s' [ID: %s] does not match the server [ID: %s]", 
                root_data.group_name, root_data.group_id, model_data.group_id
            )
            raise ValueError("local root group does not match server's root group")
        
        return model_data

    def get_children_of_group(self, group_id: uuid.UUID) -> GroupParentData:
        data: GroupPublicGet = api_get_group.sync(group_id, client=self.auth_client)
        assert data is not None

        group_data: GroupParentData = self.maindb.groups.get_children_of_group(group_id)
        model_data: GroupParentData = GroupParentData.model_validate(data, from_attributes=True)

        if group_data != model_data:
            logger.error(
                "Local group '%s' [ID: %s] does not match the server", 
                group_data.group_name, group_data.group_id
            )
            raise ValueError("local group does not match server group")
        
        return model_data

    def delete_group(self, group_id: uuid.UUID) -> bool:
        data: GenericSuccess = api_delete_group.sync(group_id, client=self.auth_client)
        assert data is not None

        self.maindb.groups.delete_group(group_id)
        return True


class PasswordEntryMethods:
    def __init__(self, parent: SyncedDatabase):
        self.parent = parent
        self.maindb = parent.maindb

        self.auth_client = parent.auth_client

    def create_entry(
        self, group_id: uuid.UUID,
        data: EditedPasswordEntryInfo
    ) -> PasswordEntryData:
        url_or_none = str(data.url) if data.url else None

        body: EntryCreate = EntryCreate(
            title=data.title, username=data.username,
            password=data.password, url=url_or_none,
            notes=data.notes
        )
        api_data: EntryPublicGet = api_create_entry.sync(
            group_id, client=self.auth_client, body=body
        )
        assert api_data is not None

        entry_public: PasswordEntryData = self.maindb.entries.create_entry(
            group_id, data, 
            entry_id=api_data.entry_id,
            created_at=api_data.created_at
        )
        return entry_public
    
    def get_entries_by_group(
        self, group_id: uuid.UUID,
        amount: int = 100, offset: int = 0
    ) -> list[PasswordEntryData]:
        data: list[EntryPublicGet] = api_get_entries.sync(
            group_id, client=self.auth_client,
            amount=amount,
            offset=offset
        )
        assert data is not None

        ta = TypeAdapter(list[PasswordEntryData])
        models = ta.validate_python(data, from_attributes=True)

        stored_entries = self.maindb.entries.get_entries_by_group(group_id, amount=amount, offset=offset)

        len_models = len(models)
        len_entries = len(stored_entries)
        
        if len_models != len_entries:
            logger.error(
                "Server returned %d entries, expected client to return the same amount of " \
                "entries, but received %d entries instead", len_models, len_entries
            )
            raise ValueError(f"expected {len_models} from client, received {len_entries} instead")
        
        return models

    def delete_entry_by_id(
        self, entry_id: uuid.UUID,
        group_id: uuid.UUID
    ) -> bool:
        data: GenericSuccess = api_delete_entry.sync(group_id, entry_id, client=self.auth_client)
        assert data is not None

        self.maindb.entries.delete_entry_by_id(entry_id, group_id)
        return True

    def update_entry_data(
        self, entry_id: uuid.UUID,
        data: EditedEntryWithGroup
    ) -> PasswordEntryData:
        url_or_none = str(data.url) if data.url else None

        body: EntryUpdate = EntryUpdate(
            title=data.title, username=data.username,
            password=data.password, url=url_or_none,
            notes=data.notes
        )
        api_data: EntryPublicGet = api_update_entry.sync(
            data.group_id, entry_id, 
            client=self.auth_client,
            body=body
        )
        assert api_data is not None

        api_model = PasswordEntryData.model_validate(api_data, from_attributes=True)
        entry_model = self.maindb.entries.update_entry_data(entry_id, data)

        if api_model != entry_model:
            logger.error(
                "Local entry '%s' [ID: %s] does not match the server model", 
                entry_model.title, entry_model.entry_id
            )
            raise ValueError("local entry does not match the server entry")
        
        return entry_model
