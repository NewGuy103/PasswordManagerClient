import logging
import uuid
from pathlib import Path

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine, select, text, true

from ..localdb.dbtables import PasswordEntry, PasswordGroups
from ..models import GroupChildrenData, GroupParentData, PasswordEntryData

logger: logging.Logger = logging.getLogger("passwordmanager-client")
DEFAULT_CHUNK_SIZE: int = 25 * 1024 * 1024  # 25 MiB


class MainDatabase:
    """Main database class. This is a local version of the server database."""
    def __init__(self):
        self.engine: Engine = None

    def setup(self, sqlite_path: Path) -> None:
        """Sets up the database and runs first-run checks.
        
        This must be called first before using the child methods.
        """

        # TODO: Add some sort of identifier so i can map local databases to multiple userrs (or non-users)
        # Or simply, build the client so that it doesnt depend on the server
        # and the server is more of an integrated sync

        self.engine = create_engine(f"sqlite:///{sqlite_path}", echo=False)
        SQLModel.metadata.create_all(self.engine)

        with Session(self.engine) as session:
            session.exec(text("PRAGMA foreign_keys=ON;"))
        
        self.groups = PasswordGroupMethods(self)
        self.entries = PasswordEntryMethods(self)

        self.groups.create_group('Root', parent_id=None)
        return

    def close(self):
        if self.engine:
            self.engine.dispose()


class PasswordGroupMethods:
    def __init__(self, parent: MainDatabase):
        self.parent = parent
        self.engine = parent.engine

    def create_group(
        self, group_name: str,
        parent_id: uuid.UUID | None = None
    ):
        with Session(self.engine) as session:
            # So the 'Root' group can be created without a parent
            if parent_id:
                result2 = session.exec(
                    select(PasswordGroups)
                    .where(PasswordGroups.group_id == parent_id)
                )
                result2.one()
            else:
                result3 = session.exec(
                    select(PasswordGroups)
                    .where(PasswordGroups.is_root == true())
                )
                root_model = result3.one_or_none()

                if root_model:
                    logger.info("Root group already exists, skipping creation...")
                    return False
            
            new_group = PasswordGroups(
                group_name=group_name,
                parent_id=parent_id,
                is_root=False if parent_id else True
            )
            session.add(new_group)
            session.commit()
        
            return self.get_children_of_group(new_group.group_id)

    def get_children_of_root(self) -> GroupParentData:
        with Session(self.engine) as session:
            result = session.exec(
                select(PasswordGroups)
                .where(PasswordGroups.is_root == true())
            )
            root_group = result.one()
            child_models: list[GroupChildrenData] = []

            # session.refresh(root_group)
            for child in root_group.child_groups:
                child_model = GroupChildrenData(
                    group_name=child.group_name,
                    parent_id=child.parent_id,
                    group_id=child.group_id
                )
                child_models.append(child_model)
            
            model = GroupParentData(
                group_name=root_group.group_name,
                parent_id=None,
                group_id=root_group.group_id,
                child_groups=child_models
            )

        return model

    def get_children_of_group(self, group_id: uuid.UUID) -> GroupParentData:
        with Session(self.engine) as session:
            result = session.exec(
                select(PasswordGroups)
                .where(
                    PasswordGroups.group_id == group_id
                )
            )
            group = result.one()

            if group.is_root:
                return self.get_children_of_root()
            
            child_models: list[GroupChildrenData] = []
            for child in group.child_groups:
                child_model = GroupChildrenData(
                    group_name=child.group_name,
                    parent_id=child.parent_id,
                    group_id=child.group_id
                )
                child_models.append(child_model)
            
            model = GroupParentData(
                group_name=group.group_name,
                parent_id=group.parent_id,
                group_id=group.group_id,
                child_groups=child_models
            )

        return model

    def delete_group(self, group_id: uuid.UUID) -> bool:
        with Session(self.engine) as session:
            result = session.exec(
                select(PasswordGroups)
                .where(
                    PasswordGroups.group_id == group_id
                )
            )
            group = result.one()

            if group.is_root:
                raise ValueError("not allowed to delete top-level group")
            
            session.delete(group)
            session.commit()

        return True


class PasswordEntryMethods:
    def __init__(self, parent: MainDatabase):
        self.parent = parent
        self.engine = parent.engine

    def create_entry(
        self, group_id: uuid.UUID,
        title: str, username: str,
        password: str, url: str,
        notes: str
    ) -> PasswordEntryData:
        with Session(self.engine) as session:
            result = session.exec(
                select(PasswordGroups)
                .where(PasswordGroups.group_id == group_id)
            )
            group = result.one()
            
            # TODO: Encrypt password entries so its safer in the database
            new_entry = PasswordEntry(
                title=title, username=username,
                password=password, url=url,
                notes=notes, group_id=group.group_id
            )
            session.add(new_entry)

            entry_public = PasswordEntryData(
                title=title, username=username,
                password=password, url=url,
                created_at=new_entry.created_at,
                notes=notes, entry_id=new_entry.entry_id,
                group_id=group.group_id
            )
            session.commit()
        
        return entry_public
    
    def get_entries_by_group(
        self, group_id: uuid.UUID,
        amount: int = 100, offset: int = 0
    ):
        with Session(self.engine) as session:
            result = session.exec(
                select(PasswordGroups)
                .where(PasswordGroups.group_id == group_id)
            )
            existing_group = result.one()

            result = session.exec(
                select(PasswordEntry, PasswordGroups)
                .join(PasswordGroups)
                .where(PasswordEntry.group_id == existing_group.group_id)
                .limit(amount)
                .offset(offset)
            )
            entries = result.all()

            entries_public: list[PasswordEntryData] = []
            for entry, group in entries:
                entry_public = PasswordEntryData(
                    title=entry.title,
                    username=entry.username,

                    password=entry.password,
                    url=entry.url,

                    created_at=entry.created_at,
                    notes=entry.notes,

                    entry_id=entry.entry_id,
                    group_id=group.group_id
                )
                entries_public.append(entry_public)
            
        return entries_public

    def delete_entry_by_id(
        self, entry_id: uuid.UUID
    ) -> bool:
        with Session(self.engine) as session:
            result = session.exec(
                select(PasswordEntry)
                .join(PasswordGroups)
                .where(
                    PasswordEntry.entry_id == entry_id
                )
            )
            entry = result.one()

            session.delete(entry)
            session.commit()
            
        return True
