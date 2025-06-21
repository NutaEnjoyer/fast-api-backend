"""
Task service module for task management operations.

This module contains the TaskService class which handles business logic
for task operations, including task creation, retrieval, updates, and
deletion. It acts as an intermediary between the API layer and the
repository layer for task-related operations.
"""

from typing import List
from app.core.database import TaskOrm
from app.dto.task_dto import CreateTaskDto, TaskDto, UpdateTaskDto
from app.repository.task_repository import TaskRepository
from app.services.base_service import BaseService


class TaskService(BaseService):
    """
    Service class for task management operations.

    This class handles business logic for task operations, including
    task creation, retrieval, updates, and deletion. It provides
    a clean interface for task-related operations and handles
    data transformation between ORM models and DTOs.

    The TaskService acts as an intermediary between the API layer
    and the repository layer, ensuring proper data validation and
    business rule enforcement.
    """

    def __init__(self, task_repository: TaskRepository = TaskRepository()):
        """
        Initialize the task service.

        Args:
            task_repository: Repository for task operations
        """
        self.task_repository = task_repository

    def _to_dto(self, task: TaskOrm) -> TaskDto:
        """
        Convert TaskOrm to TaskDto.

        Args:
            task: Task ORM model instance

        Returns:
            Task DTO instance
        """
        return TaskDto.model_validate(task)

    async def create(self, user_id: str, dto: CreateTaskDto) -> TaskDto:
        """
        Create a new task for a user.

        Args:
            user_id: ID of the user who owns the task
            dto: Task creation data

        Returns:
            Created task DTO

        Raises:
            ValidationError: If task data is invalid
            SQLAlchemyError: If database operation fails
        """
        task = await self.task_repository.create(user_id, dto)
        return self._to_dto(task)

    async def get_all(self, user_id: str) -> List[TaskDto]:
        """
        Get all tasks for a specific user.

        Args:
            user_id: ID of the user whose tasks to retrieve

        Returns:
            List of task DTOs belonging to the user

        Note:
            Returns empty list if user has no tasks or if database
            operation fails.
        """
        tasks = await self.task_repository.get_all(user_id)
        tasks = [self._to_dto(task) for task in tasks]
        return tasks

    async def update(self, user_id: str, id: str, task: UpdateTaskDto) -> TaskDto:
        """
        Update an existing task.

        Args:
            user_id: ID of the user who owns the task
            id: Task's unique identifier
            task: Updated task data

        Returns:
            Updated task DTO

        Raises:
            NotFoundException: If task with specified ID is not found
            ValidationError: If task data is invalid
            SQLAlchemyError: If database operation fails
        """
        updated_task = await self.task_repository.update(user_id, id, task)
        return self._to_dto(updated_task)

    async def delete(self, user_id: str, id: str) -> str:
        """
        Delete a task from the database.

        Args:
            user_id: ID of the user who owns the task
            id: Task's unique identifier

        Returns:
            ID of the deleted task

        Note:
            This operation is irreversible and will permanently remove
            the task. No exception is raised if task doesn't exist.
        """
        await self.task_repository.delete(user_id, id)
        return id
