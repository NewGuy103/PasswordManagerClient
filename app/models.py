import uuid

from pydantic import BaseModel


# State models
class PasswordEntryBase(BaseModel):
    entry_name: str
    username: str

    password: str
    url: str


class AddPasswordEntry(PasswordEntryBase):
    pass


class PasswordEntryData(PasswordEntryBase):
    entry_id: uuid.UUID
    # group_id: uuid.UUID
    pass


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
