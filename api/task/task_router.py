from typing import Annotated, List
from fastapi import APIRouter, Depends

from dto.task_dto import CreateTaskDto, CreateTaskResponseDto, TaskDto, TaskResponseDto
from repository.task_repository import TaskRepository
from services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])

task_service = TaskService()

@router.get("", response_model=TaskResponseDto, status_code=200)
async def get_task() -> List[TaskDto]:
    tasks = await task_service.get_all()
    return {"ok": True, "tasks": tasks}
    

@router.post('', response_model=CreateTaskResponseDto, status_code=201)
async def create_task(task: Annotated[CreateTaskDto, Depends()]) -> CreateTaskResponseDto:
    id = await task_service.create(task)
    return {"ok": True, "task_id": id}
