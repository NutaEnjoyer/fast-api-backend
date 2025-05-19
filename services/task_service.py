from typing import List
from dto.task_dto import CreateTaskDto, TaskDto
from repository.task_repository import TaskRepository
from services.base_service import BaseService


class TaskService(BaseService):
    def __init__(self, task_repository: TaskRepository = TaskRepository()):
        self.task_repository = task_repository

    async def create(self, task: CreateTaskDto) -> str:
        id = await self.task_repository.create(task)
        return id

    async def get_all(self) -> List[TaskDto]:
        tasks = await self.task_repository.get_all()
        tasks = [TaskDto.model_validate(task) for task in tasks]
        return tasks
    