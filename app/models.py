import uuid

from datetime import datetime, timezone
from pydantic import BaseModel, AwareDatetime


# State models
class PasswordEntryBase(BaseModel):
    """Base for password entries."""
    title: str
    username: str

    password: str
    url: str

    notes: str


class AddPasswordEntry(PasswordEntryBase):
    """Add password entry dialog."""
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
