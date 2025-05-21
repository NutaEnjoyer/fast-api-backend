from typing import List
from app.core.database import TaskOrm
from app.dto.task_dto import CreateTaskDto, TaskDto, UpdateTaskDto
from app.repository.task_repository import TaskRepository
from app.services.base_service import BaseService


class TaskService(BaseService):
    def __init__(self, task_repository: TaskRepository = TaskRepository()):
        self.task_repository = task_repository

    def _to_dto(self, task: TaskOrm) -> TaskDto:
        return TaskDto.model_validate(task)

    async def create(self, user_id: str, dto: CreateTaskDto) -> TaskDto:
        task = await self.task_repository.create(user_id, dto)
        print("TASK ORM: ", task)
        res = self._to_dto(task)
        print("TASK DTO: ", res)
        return self._to_dto(task)

    async def get_all(self, user_id) -> List[TaskDto]:
        tasks = await self.task_repository.get_all(user_id)
        tasks = [self._to_dto(task) for task in tasks]
        return tasks
    
    async def update(self, user_id: str, id: str, task: UpdateTaskDto) -> TaskDto:
        task = await self.task_repository.update(user_id, id, task)
        return self._to_dto(task)
    
    async def delete(self, user_id: str, id: str) -> str:
        await self.task_repository.delete(user_id, id)
        return id
