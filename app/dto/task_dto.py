"""
Task DTO (Data Transfer Object) module.

This module provides DTOs for task-related operations including
creation, updates, responses, and data validation for task management.
"""

from pydantic import BaseModel
from enum import Enum

from app.dto.base_dto import BaseDto, BaseModelDto
from app.dto.response_dto import ResponseDto


class Priority(str, Enum):
    """
    Task priority levels.

    Defines the available priority levels for tasks
    with corresponding string values for API responses.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreateTaskDto(BaseModelDto):
    """
    DTO for creating new tasks.

    Contains all required and optional fields needed
    to create a new task in the system.
    """

    title: str
    description: str | None = None
    priority: Priority | None = None
    is_completed: bool = False


class TaskDto(CreateTaskDto, BaseDto):
    """
    Complete task DTO with all fields.

    Extends CreateTaskDto with base fields (id, timestamps)
    and includes the user_id relationship.
    """

    user_id: str


class ListTaskResponseDto(ResponseDto):
    """
    Response DTO for task list operations.

    Contains a list of tasks with success status.
    """

    tasks: list[TaskDto]


class TaskResponseDto(ResponseDto):
    """
    Response DTO for single task operations.

    Contains a single task with success status.
    """

    task: TaskDto


class UpdateTaskDto(CreateTaskDto):
    """
    DTO for updating existing tasks.

    All fields are optional to allow partial updates
    of task properties.
    """

    title: str | None = None


class DeleteTaskResponseDto(ResponseDto):
    """
    Response DTO for task deletion operations.

    Contains the ID of the deleted task with success status.
    """

    id: str
