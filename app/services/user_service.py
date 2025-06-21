"""
User service module for user management operations.

This module contains the UserService class which handles business logic
for user operations, including user creation, retrieval, updates,
deletion, and user statistics. It acts as an intermediary between
the API layer and the repository layer for user-related operations.
"""

from sqlalchemy import and_, func, select
from app.core.database import TaskOrm, UserOrm
from app.dto.auth_dto import AuthDto
from app.dto.user_dto import GetUserDto, UpdateUserDto, UserDto
from app.repository.user_repository import UserRepository
from app.utils.date import get_start_datetime
from exceptions import NotFoundException


class UserService:
    """
    Service class for user management operations.

    This class handles business logic for user operations, including
    user creation, retrieval, updates, deletion, and user statistics.
    It provides a clean interface for user-related operations and
    handles data transformation between ORM models and DTOs.

    The UserService acts as an intermediary between the API layer
    and the repository layer, ensuring proper data validation and
    business rule enforcement for user management.
    """

    def __init__(self, user_repository: UserRepository = UserRepository()):
        """
        Initialize the user service.

        Args:
            user_repository: Repository for user operations
        """
        self.user_repository = user_repository

    def _to_dto(self, user: UserOrm) -> UserDto:
        """
        Convert UserOrm to UserDto.

        Args:
            user: User ORM model instance

        Returns:
            User DTO instance
        """
        return UserDto.model_validate(user)

    async def create(self, dto: AuthDto) -> UserDto:
        """
        Create a new user.

        Args:
            dto: Authentication data containing user information

        Returns:
            Created user DTO

        Raises:
            ValidationError: If user data is invalid
            SQLAlchemyError: If database operation fails
        """
        user = await self.user_repository.create(dto)
        return self._to_dto(user)

    async def get_me(self, id: str) -> GetUserDto:
        """
        Get current user information with task statistics.

        This method retrieves user information along with task statistics
        for today and the current week, providing a comprehensive view
        of the user's activity.

        Args:
            id: User's unique identifier

        Returns:
            User DTO with task statistics

        Raises:
            NotFoundException: If user with specified ID is not found
        """
        user = await self.user_repository.find_by_id(id)
        if not user:
            raise NotFoundException(
                detail="User with this id not found",
                resource_type="User",
                resource_id=id,
            )

        today_start, week_start = get_start_datetime()
        today_start = int(today_start.timestamp())
        week_start = int(week_start.timestamp())
        total_tasks, completed_tasks, today_tasks, week_tasks = (
            await self.user_repository.get_tasks_statistic(id, today_start, week_start)
        )

        return GetUserDto(
            **UserDto.model_validate(user).model_dump(),
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            today_tasks=today_tasks,
            week_tasks=week_tasks,
        )

    async def find_by_id(self, id: str) -> UserDto:
        """
        Find a user by their ID.

        Args:
            id: User's unique identifier

        Returns:
            User DTO if found

        Raises:
            NotFoundException: If user with specified ID is not found
        """
        user = await self.user_repository.find_by_id(id)
        if not user:
            raise NotFoundException(
                detail="User with this id not found",
                resource_type="User",
                resource_id=id,
            )
        return self._to_dto(user)

    async def find_by_email(self, email: str) -> UserDto:
        """
        Find a user by their email address.

        Args:
            email: User's email address

        Returns:
            User DTO if found

        Raises:
            NotFoundException: If user with specified email is not found
        """
        user = await self.user_repository.find_by_email(email)
        if not user:
            raise NotFoundException(
                detail="User with this email not found",
                resource_type="User",
                resource_id=email,
            )
        return self._to_dto(user)

    async def update(self, id: str, dto: UpdateUserDto) -> UserDto:
        """
        Update user information.

        Args:
            id: User's unique identifier
            dto: Updated user data

        Returns:
            Updated user DTO

        Raises:
            NotFoundException: If user with specified ID is not found
            ValidationError: If user data is invalid
            SQLAlchemyError: If database operation fails
        """
        # Check if user exists before updating
        existing_user = await self.user_repository.find_by_id(id)
        if not existing_user:
            raise NotFoundException(
                detail="User with this id not found",
                resource_type="User",
                resource_id=id,
            )

        user = await self.user_repository.update(id, dto)
        return self._to_dto(user)

    async def delete(self, id: str) -> str:
        """
        Delete a user from the database.

        Args:
            id: User's unique identifier

        Returns:
            ID of the deleted user

        Note:
            This operation is irreversible and will permanently remove
            the user and all associated data (tasks, pomodoro sessions, etc.).
            No exception is raised if user doesn't exist.
        """
        await self.user_repository.delete(id)
        return id
