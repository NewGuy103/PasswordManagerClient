import uuid

from datetime import datetime, timezone
from pydantic import BaseModel, AwareDatetime, HttpUrl, AnyUrl


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


class PasswordEntryData(PasswordEntryBase):
    entry_id: uuid.UUID
    group_id: uuid.UUID
    created_at: AwareDatetime = datetime.now(timezone.utc)


# TODO: Extend this when adding metadata
class AddPasswordGroup(BaseModel):
    group_name: str


class GroupBase(BaseModel):
    group_id: uuid.UUID
    group_name: str
    parent_id: uuid.UUID | None


class GroupParentData(GroupBase):
    child_groups: list['GroupChildrenData']


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


class SaveSyncInfo(SyncBase):
    server_url: HttpUrl
    access_token: str
    sync_enabled: bool
