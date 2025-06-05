import logging
import secrets
import typing
import uuid
from datetime import datetime, timezone

from sqlalchemy import Engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel import Session, SQLModel, create_engine, select

from ..config import app_file_paths

logger: logging.Logger = logging.getLogger("passwordmanager-client")
DEFAULT_CHUNK_SIZE: int = 25 * 1024 * 1024  # 25 MiB


class MainDatabase:
    """Main database class. This is a local version of the server database."""
    def __init__(self):
        self.engine: Engine = None

    def setup(self):
        """Sets up the database and runs first-run checks.
        
        This must be called first before using the child methods.
        """

        SQLModel.metadata.create_all()

        # TODO: Add some sort of identifier so i can map local databases to multiple userrs (or non-users)
        # Or simply, build the client so that it doesnt depend on the server
        # and the server is more of an integrated sync
        self.engine = create_engine(f"sqlite:///{app_file_paths.sqlite_file}")

        self.groups = PasswordGroupMethods(self)
        self.entries = PasswordEntryMethods(self)

    def close(self):
        self.engine.dispose()


class PasswordGroupMethods:
    def __init__(self, parent: MainDatabase):
        self.parent = parent
        self.engine = parent.engine


class PasswordEntryMethods:
    def __init__(self, parent: MainDatabase):
        self.parent = parent
        self.engine = parent.engine


database: MainDatabase = MainDatabase()
