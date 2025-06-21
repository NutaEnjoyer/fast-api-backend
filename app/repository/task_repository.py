"""
Task repository module for task-related database operations.

This module contains the TaskRepository class which handles all database
operations related to tasks, including CRUD operations and task management.
"""

from typing import List

from sqlalchemy import and_, select, delete
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import TaskOrm
from app.dto.task_dto import CreateTaskDto, UpdateTaskDto
from app.repository.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """
    Repository class for task-related database operations.

    This class provides methods for creating, reading, updating, and deleting
    tasks, as well as managing task relationships with users.
    """

    async def create(self, user_id: str, data: CreateTaskDto) -> TaskOrm:
        """
        Create a new task for a user.

        Args:
            user_id: ID of the user who owns the task
            data: Task creation data

        Returns:
            Created task object

        Raises:
            SQLAlchemyError: If database operation fails
        """
        async with self.session() as session:
            task_dict = data.model_dump()
            task_dict["user_id"] = user_id

            task = TaskOrm(**task_dict)
            session.add(task)

            await session.flush()
            await session.commit()
            await session.refresh(task)

            return task

    async def get_all(self, user_id: str) -> List[TaskOrm]:
        """
        Get all tasks for a specific user.

        Args:
            user_id: ID of the user whose tasks to retrieve

        Returns:
            List of task objects belonging to the user
        """
        async with self.session() as session:
            query = select(TaskOrm).where(TaskOrm.user_id == user_id)
            result = await session.execute(query)
            tasks_models = list(result.scalars().all())
            return tasks_models

    async def update(self, user_id: str, id: str, data: UpdateTaskDto) -> TaskOrm:
        """
        Update an existing task.

        Args:
            user_id: ID of the user who owns the task
            id: Task's unique identifier
            data: Updated task data

        Returns:
            Updated task object

        Raises:
            ValueError: If task with the specified ID is not found
            RuntimeError: If database operation fails
        """
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(TaskOrm).where(
                        and_(TaskOrm.id == id, TaskOrm.user_id == user_id)
                    )
                )

                task = result.scalars().first()

                if not task:
                    raise ValueError(f"Task with id {id} not found")

                update_data = data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(task, key, value)

                await session.flush()
                await session.commit()
                await session.refresh(task)
                return task

            except SQLAlchemyError as e:
                await session.rollback()
                raise RuntimeError(f"Database error: {str(e)}")

    async def delete(self, user_id: str, id: str) -> str:
        """
        Delete a task from the database.

        Args:
            user_id: ID of the user who owns the task
            id: Task's unique identifier

        Returns:
            ID of the deleted task

        Note:
            This operation is irreversible and will permanently remove the task.
        """
        async with self.session() as session:
            result = await session.execute(
                delete(TaskOrm).where(
                    and_(TaskOrm.id == id, TaskOrm.user_id == user_id)
                )
            )

            await session.commit()
            return id
