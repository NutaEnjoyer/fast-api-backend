from typing import List

from sqlalchemy import and_, select, delete
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import TaskOrm
from app.dto.task_dto import CreateTaskDto, TaskDto, UpdateTaskDto
from app.repository.base_repository import BaseRepository


class TaskRepository(BaseRepository):

    async def create(self, user_id: str, data: CreateTaskDto) -> TaskOrm:
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
        async with self.session() as session:
            query = select(TaskOrm).where(TaskOrm.user_id == user_id)
            result = await session.execute(query)
            tasks_models = result.scalars().all()
            return tasks_models
        
    async def update(self, user_id: str, id: str, data: UpdateTaskDto) -> TaskOrm:
        async with self.session() as session: 
            try:
                result = await session.execute(
                    select(TaskOrm).where(
                        and_(
                            TaskOrm.id == id,
                            TaskOrm.user_id == user_id
                        )
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
        async with self.session() as session:
            result = await session.execute(
                delete(TaskOrm).where(
                    and_(
                        TaskOrm.id == id,
                        TaskOrm.user_id == user_id
                    )
                )
            )
        
            await session.commit()
            return id
