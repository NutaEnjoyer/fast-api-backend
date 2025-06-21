"""
User repository module for user-related database operations.

This module contains the UserRepository class which handles all database
operations related to users, including CRUD operations and user statistics.
"""

from typing import Tuple
from sqlalchemy import and_, delete, func, select
from app.core.database import TaskOrm, UserOrm
from app.dto.auth_dto import AuthDto
from app.dto.user_dto import UpdateUserDto
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """
    Repository class for user-related database operations.

    This class provides methods for creating, reading, updating, and deleting
    users, as well as retrieving user statistics and task information.
    """

    async def create(self, data: AuthDto) -> UserOrm:
        """
        Create a new user in the database.

        Args:
            data: Authentication data containing user information

        Returns:
            Created user object

        Raises:
            ValueError: If user with the same email already exists
        """
        async with self.session() as session:
            user = UserOrm(**data.model_dump())
            session.add(user)
            await session.flush()
            await session.commit()
            await session.refresh(user)
            return user

    async def find_by_email(self, email: str) -> UserOrm | None:
        """
        Find a user by their email address.

        Args:
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        async with self.session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    async def find_by_id(self, id: str) -> UserOrm | None:
        """
        Find a user by their ID.

        Args:
            id: User's unique identifier

        Returns:
            User object if found, None otherwise
        """
        async with self.session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    async def get_tasks_statistic(
        self, id: str, today_start: int, week_start: int
    ) -> Tuple[int, int, int, int]:
        """
        Get task statistics for a user.

        Args:
            id: User's unique identifier
            today_start: Timestamp for the start of today
            week_start: Timestamp for the start of the week

        Returns:
            Tuple containing (total_tasks, completed_tasks, today_tasks, week_tasks)
        """
        async with self.session() as session:
            total_tasks = (
                await session.scalar(
                    select(func.count(TaskOrm.id)).where(TaskOrm.user_id == id)
                )
                or 0
            )

            completed_tasks = (
                await session.scalar(
                    select(func.count(TaskOrm.id)).where(
                        and_(TaskOrm.user_id == id, TaskOrm.is_completed.isnot(None))
                    )
                )
                or 0
            )

            today_tasks = (
                await session.scalar(
                    select(func.count(TaskOrm.id)).where(
                        and_(TaskOrm.user_id == id, TaskOrm.created_at >= today_start)
                    )
                )
                or 0
            )

            week_tasks = (
                await session.scalar(
                    select(func.count(TaskOrm.id)).where(
                        and_(TaskOrm.user_id == id, TaskOrm.created_at >= week_start)
                    )
                )
                or 0
            )

            return total_tasks, completed_tasks, today_tasks, week_tasks

    async def update(self, id: str, data: UpdateUserDto) -> UserOrm:
        """
        Update user information.

        Args:
            id: User's unique identifier
            data: Updated user data

        Returns:
            Updated user object

        Raises:
            ValueError: If user with the specified ID is not found
        """
        async with self.session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            result = await session.execute(query)
            user = result.scalars().first()

            if not user:
                raise ValueError(f"User with id {id} not found")

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(user)
            return user

    async def delete(self, id: str) -> None:
        """
        Delete a user from the database.

        Args:
            id: User's unique identifier

        Note:
            This operation is irreversible and will remove all user data.
        """
        async with self.session() as session:
            query = delete(UserOrm).where(UserOrm.id == id)
            await session.execute(query)

            await session.commit()
