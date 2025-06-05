import uuid
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


# Self referential model (https://docs.sqlalchemy.org/en/latest/orm/self_referential.html)
class PasswordGroups(SQLModel, table=True):
    group_id: uuid.UUID = Field(primary_key=True)
    group_name: str = Field(min_length=1, nullable=False, index=True)

    parent_id: uuid.UUID | None = Field(foreign_key='passwordgroups.group_id', ondelete='CASCADE')

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
    entry_name: str = Field(min_length=1, nullable=False, index=True)

    entry_data: str = Field(min_length=1, nullable=False)

    group_id: uuid.UUID = Field(foreign_key='passwordgroups.group_id', ondelete='CASCADE')
    group: PasswordGroups = Relationship(
        back_populates='entries',
        sa_relationship_kwargs={'lazy': 'selectin'}
    )

