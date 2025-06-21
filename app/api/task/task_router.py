from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.dto.task_dto import *
from app.repository.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service() -> TaskService:
    repository = TaskRepository()
    return TaskService(repository)


@router.get("", response_model=ListTaskResponseDto, status_code=status.HTTP_200_OK)
async def get_tasks(
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> ListTaskResponseDto:
    tasks = await service.get_all(current_user)
    return {"ok": True, "tasks": tasks}


@router.post("", response_model=TaskResponseDto, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: CreateTaskDto,
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> TaskResponseDto:
    task = await service.create(current_user, task)
    return {"ok": True, "task": task}


@router.put("/{id}", response_model=TaskResponseDto, status_code=status.HTTP_200_OK)
async def update_task(
    id: str,
    task: UpdateTaskDto,
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> TaskResponseDto:
    task: TaskDto = await service.update(current_user, id, task)
    return {"ok": True, "task": task}


@router.delete(
    "/{id}", response_model=DeleteTaskResponseDto, status_code=status.HTTP_200_OK
)
async def delete_task(
    id: str,
    service: TaskService = Depends(get_task_service),
    current_user: str = Depends(get_current_user),
) -> DeleteTaskResponseDto:
    await service.delete(current_user, id)
    return {"ok": True, "id": id}
