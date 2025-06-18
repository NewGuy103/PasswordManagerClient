import uuid
from typing import Optional
from datetime import timezone, datetime

from sqlmodel import Column, SQLModel, Field, DateTime, Relationship, TypeDecorator


class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=timezone.utc)
        return value


# Self referential model (https://docs.sqlalchemy.org/en/latest/orm/self_referential.html)
class PasswordGroups(SQLModel, table=True):
    group_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    group_name: str = Field(min_length=1, nullable=False, index=True)

    parent_id: uuid.UUID | None = Field(foreign_key='passwordgroups.group_id', ondelete='CASCADE')
    is_root: bool = Field()

    # Self-referential relationships
    parent_group: Optional['PasswordGroups'] = Relationship(
        back_populates='child_groups',
        sa_relationship_kwargs={'lazy': 'selectin', 'remote_side': 'PasswordGroups.group_id'}
    )
    child_groups: list['PasswordGroups'] = Relationship(
        back_populates='parent_group',
        sa_relationship_kwargs={'lazy': 'selectin'},
        passive_deletes='all'
    )
    
    entries: list['PasswordEntry'] = Relationship(
        back_populates='group',
        sa_relationship_kwargs={'lazy': 'selectin'},
        passive_deletes='all'
    )


class PasswordEntry(SQLModel, table=True):
    entry_id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    title: str = Field(nullable=False, index=True)

    username: str = Field(nullable=False)
    password: str = Field(nullable=False)  # keep this encrypted
    
    url: str = Field(nullable=False)
    notes: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TZDateTime)
    )

    group_id: uuid.UUID = Field(foreign_key='passwordgroups.group_id', ondelete='CASCADE')
    group: PasswordGroups = Relationship(
        back_populates='entries',
        sa_relationship_kwargs={'lazy': 'selectin'}
    )
