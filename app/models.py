import uuid
from datetime import UTC, datetime

from pydantic import AnyUrl, AwareDatetime, BaseModel, HttpUrl


# State models
class PasswordEntryBase(BaseModel):
    """Base for password entries."""

    title: str
    username: str

    password: str
    url: AnyUrl | None = None

    notes: str


class EditedPasswordEntryInfo(PasswordEntryBase):
    pass


class EditedEntryWithGroup(EditedPasswordEntryInfo):
    entry_id: uuid.UUID
    group_id: uuid.UUID


class PasswordEntryData(PasswordEntryBase):
    entry_id: uuid.UUID
    group_id: uuid.UUID
    created_at: AwareDatetime = datetime.now(UTC)


# TODO: Extend this when adding metadata
class AddPasswordGroup(BaseModel):
    group_name: str


class GroupBase(BaseModel):
    group_id: uuid.UUID
    group_name: str
    parent_id: uuid.UUID | None


class GroupParentData(GroupBase):
    child_groups: list["GroupChildrenData"]


# Leave out child_groups intentionally
class GroupChildrenData(GroupBase):
    parent_id: uuid.UUID


# Sync info
class SyncBase(BaseModel):
    username: str
    server_url: HttpUrl | None = None


class SyncInfo(SyncBase):
    sync_enabled: bool = False


class TestSyncAuth(SyncBase):
    server_url: HttpUrl
    password: str


class SavedSyncInfo(SyncBase):
    server_url: HttpUrl
    access_token: str
    sync_enabled: bool
