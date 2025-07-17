import logging
import uuid

import httpx
from pydantic import TypeAdapter

from ..client import AuthenticatedClient
from ..client import models as api_models  # Generated client models
from ..client.api.auth import auth_test_api_auth_test_auth_get as auth_test
from ..client.api.groups import change_entry_data_api_groups_group_id_entries_entry_id_put as api_update_entry

# groups
from ..client.api.groups import create_group_api_groups_post as api_create_group

# entries (under groups)
from ..client.api.groups import create_password_entry_api_groups_group_id_entries_post as api_create_entry
from ..client.api.groups import delete_group_api_groups_group_id_delete as api_delete_group
from ..client.api.groups import delete_password_entry_api_groups_group_id_entries_entry_id_delete as api_delete_entry
from ..client.api.groups import get_group_children_api_groups_group_id_children_get as api_get_group
from ..client.api.groups import get_group_entries_api_groups_group_id_entries_get as api_get_entries
from ..client.api.groups import retrieve_top_level_groups_api_groups_get as api_get_root_group
from ..client.models import UserInfoPublic
from ..client.types import Response
from ..models import EditedEntryWithGroup, EditedPasswordEntryInfo, SavedSyncInfo
from . import models as pd_models  # Generated Pydantic models

logger: logging.Logger = logging.getLogger("passwordmanager-client")
DEFAULT_CHUNK_SIZE: int = 25 * 1024 * 1024  # 25 MiB


class SyncClient:
    """Abstraction to syncing with the server, separating the local database and the server sync."""

    def __init__(self):
        self.auth_client: AuthenticatedClient = None

    def setup(self, sync_info: SavedSyncInfo) -> None:
        self.auth_client: AuthenticatedClient = AuthenticatedClient(
            str(sync_info.server_url),
            sync_info.access_token,
            raise_on_unexpected_status=True,
            timeout=30,
            httpx_args={"event_hooks": {"request": [self.log_request], "response": [self.log_response]}},
        )
        data: Response[UserInfoPublic] = auth_test.sync_detailed(client=self.auth_client)

        if data.parsed is None:
            raise ValueError("Invalid data from server during setup")

        if data.parsed.username != sync_info.username:
            raise ValueError("Username from sync info does not match the server")

        self.groups = PasswordGroupMethods(self)
        self.entries = PasswordEntryMethods(self)

        return

    def log_request(self, req: httpx.Request):
        headers = dict(req.headers)
        if headers.get("authorization"):
            headers["authorization"] = "..."

        logger.debug("HTTP request sent: [%s %s] - Headers: %s", req.method, req.url, headers)

    def log_response(self, res: httpx.Response):
        req = res.request
        logger.debug(
            "HTTP response received from request [%s %s] - Status Code %d - Headers: %s",
            req.method,
            req.url,
            res.status_code,
            dict(res.headers),
        )

    def close(self):
        if self.auth_client:
            self.auth_client.get_httpx_client().close()
            logger.debug("Closed HTTP client")


class PasswordGroupMethods:
    def __init__(self, parent: SyncClient):
        self.parent = parent
        self.auth_client = parent.auth_client

    def create_group(self, group_name: str, parent_id: uuid.UUID) -> pd_models.GroupPublicModify:
        body = api_models.GroupCreate(group_name=group_name, parent_id=parent_id)
        data: api_models.GroupPublicModify = api_create_group.sync(client=self.auth_client, body=body)
        assert data is not None

        model = pd_models.GroupPublicModify.model_validate(data, from_attributes=True)
        return model

    def get_children_of_root(self) -> pd_models.GroupPublicGet:
        data: api_models.GroupPublicGet = api_get_root_group.sync(client=self.auth_client)
        assert data is not None

        model = pd_models.GroupPublicGet.model_validate(data, from_attributes=True)
        return model

    def get_children_of_group(self, group_id: uuid.UUID) -> pd_models.GroupPublicGet:
        data: api_models.GroupPublicGet = api_get_group.sync(group_id, client=self.auth_client)
        assert data is not None

        model_data: pd_models.GroupPublicGet = pd_models.GroupPublicGet.model_validate(data, from_attributes=True)
        return model_data

    def delete_group(self, group_id: uuid.UUID) -> pd_models.GenericSuccess:
        data: api_models.GenericSuccess = api_delete_group.sync(group_id, client=self.auth_client)
        assert data is not None

        model: pd_models.GenericSuccess = pd_models.GenericSuccess.model_validate(data, from_attributes=True)
        return model


class PasswordEntryMethods:
    def __init__(self, parent: SyncClient):
        self.parent = parent
        self.auth_client = parent.auth_client

    def create_entry(self, group_id: uuid.UUID, data: EditedPasswordEntryInfo) -> pd_models.EntryPublicGet:
        url_or_none = str(data.url) if data.url else None

        body: api_models.EntryCreate = api_models.EntryCreate(
            title=data.title, username=data.username, password=data.password, url=url_or_none, notes=data.notes
        )
        api_data: api_models.EntryPublicGet = api_create_entry.sync(group_id, client=self.auth_client, body=body)
        assert api_data is not None

        model = pd_models.EntryPublicGet.model_validate(api_data, from_attributes=True)
        return model

    def get_entries_by_group(
        self, group_id: uuid.UUID, amount: int = 100, offset: int = 0
    ) -> list[pd_models.EntryPublicGet]:
        data: list[api_models.EntryPublicGet] = api_get_entries.sync(
            group_id, client=self.auth_client, amount=amount, offset=offset
        )
        assert data is not None

        ta = TypeAdapter(list[pd_models.EntryPublicGet])
        models = ta.validate_python(data, from_attributes=True)

        return models

    def delete_entry_by_id(self, entry_id: uuid.UUID, group_id: uuid.UUID) -> pd_models.GenericSuccess:
        data: api_models.GenericSuccess = api_delete_entry.sync(group_id, entry_id, client=self.auth_client)
        assert data is not None

        model = pd_models.GenericSuccess.model_validate(data, from_attributes=True)
        return model

    def update_entry_data(self, entry_id: uuid.UUID, data: EditedEntryWithGroup) -> pd_models.EntryPublicGet:
        url_or_none = str(data.url) if data.url else None

        body: api_models.EntryUpdate = api_models.EntryUpdate(
            title=data.title, username=data.username, password=data.password, url=url_or_none, notes=data.notes
        )
        api_data: api_models.EntryPublicGet = api_update_entry.sync(
            data.group_id, entry_id, client=self.auth_client, body=body
        )
        assert api_data is not None

        model = pd_models.EntryPublicGet.model_validate(api_data, from_attributes=True)
        return model
