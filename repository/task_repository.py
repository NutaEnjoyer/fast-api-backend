from typing import List

from sqlalchemy import select
from database import TaskOrm
from dto.task_dto import CreateTaskDto, TaskDto
from repository.base_repository import BaseRepository

class TaskRepository(BaseRepository):

    async def create(self, data: CreateTaskDto) -> str:
        async with self.session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)

            await session.flush()
            await session.commit()

            return task.id


    async def get_all(self) -> List[TaskDto]:
        async with self.session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            tasks_models = result.scalars().all()
            return tasks_models
