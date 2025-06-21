"""
Task API router module.

This module provides task-related API endpoints including
CRUD operations for task management with proper authentication,
validation, and error handling.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from app.dto.task_dto import *
from app.repository.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.dependencies.auth import get_current_user


# Task API router with prefix and tags
router = APIRouter(
    prefix="/tasks",
    tags=["Task Management"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
    },
)


def get_task_service() -> TaskService:
    """
    Dependency injection for TaskService.

    Creates and returns a TaskService instance with
    a TaskRepository dependency.

    Returns:
        TaskService: Configured task service instance
    """
    repository = TaskRepository()
    return TaskService(repository)


@router.get(
    "",
    response_model=ListTaskResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieve all tasks for the authenticated user",
)
async def get_tasks(
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> ListTaskResponseDto:
    """
    Get all tasks for the current user.

    Retrieves all tasks belonging to the authenticated user
    with their complete information and status.

    Args:
        service: Task service dependency
        current_user: Current user ID from JWT token

    Returns:
        ListTaskResponseDto: List of user's tasks

    Raises:
        HTTPException: If retrieval fails or user unauthorized
    """
    try:
        tasks = await service.get_all(current_user)
        return ListTaskResponseDto.model_validate(tasks)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks",
        )


@router.post(
    "",
    response_model=TaskResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Create a new task for the authenticated user",
)
async def create_task(
    task_data: CreateTaskDto,
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> TaskResponseDto:
    """
    Create a new task.

    Creates a new task for the authenticated user with
    the provided task information and preferences.

    Args:
        task_data: Task creation data transfer object
        service: Task service dependency
        current_user: Current user ID from JWT token

    Returns:
        TaskResponseDto: Created task information

    Raises:
        HTTPException: If task creation fails or validation error
    """
    try:
        task: TaskDto = await service.create(current_user, task_data)
        return TaskResponseDto.model_validate(task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


@router.put(
    "/{id}",
    response_model=TaskResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update a task by its ID",
)
async def update_task(
    id: str,
    task_data: UpdateTaskDto,
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> TaskResponseDto:
    """
    Update an existing task.

    Updates a task belonging to the authenticated user
    with the provided task information. All fields are optional
    for partial updates.

    Args:
        id: Task ID to update
        task_data: Task update data transfer object
        service: Task service dependency
        current_user: Current user ID from JWT token

    Returns:
        TaskResponseDto: Updated task information

    Raises:
        HTTPException: If task not found, update fails, or unauthorized
    """
    try:
        task: TaskDto = await service.update(current_user, id, task_data)
        return TaskResponseDto.model_validate(task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


@router.delete(
    "/{id}",
    response_model=DeleteTaskResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Delete a task",
    description="Delete a task by its ID",
)
async def delete_task(
    id: str,
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> DeleteTaskResponseDto:
    """
    Delete a task.

    Permanently deletes a task belonging to the authenticated user.
    This action cannot be undone.

    Args:
        id: Task ID to delete
        service: Task service dependency
        current_user: Current user ID from JWT token

    Returns:
        DeleteTaskResponseDto: Confirmation of deletion with task ID

    Raises:
        HTTPException: If task not found, deletion fails, or unauthorized
    """
    try:
        await service.delete(current_user, id)
        return DeleteTaskResponseDto.model_validate({"id": id})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )
