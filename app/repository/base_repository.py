"""
Base repository module providing common database operations.

This module contains the BaseRepository class which serves as a foundation
for all repository classes in the application, providing common database
session management and basic CRUD operations.
"""

from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.core.database import new_session, BaseModel

TypeOrm = TypeVar("TypeOrm", bound=BaseModel)


class BaseRepository:
    """
    Base repository class providing common database operations.

    This class serves as a foundation for all repository classes,
    providing database session management and common patterns for
    database operations.

    Attributes:
        session: Async session maker for database operations
    """

    def __init__(self, session: async_sessionmaker[AsyncSession] = new_session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: Async session maker for database operations.
                    Defaults to the application's session maker.
        """
        self.session = session
