from sqlalchemy import and_, func, select
from app.core.database import TaskOrm, UserOrm
from app.dto.auth_dto import AuthDto
from app.dto.user_dto import GetUserDto, UpdateUserDto, UserDto
from app.repository.user_repository import UserRepository
from app.utils.date import get_start_datetime


class UserService():
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    def _to_dto(self, user: UserOrm) -> UserDto:
        return UserDto.model_validate(user)
    
    async def create(self, dto: AuthDto) -> UserDto:
        user = await self.user_repository.create(dto)
        return self._to_dto(user)
    
    async def get_me(self, id: str) -> GetUserDto:
        user = await self.user_repository.find_by_id(id)

        today_start, week_start = get_start_datetime()
        total_tasks, completed_tasks, today_tasks, week_tasks = await self.user_repository.get_tasks_statistic(id, today_start, week_start)

        return GetUserDto(
            **UserDto.model_validate(user).model_dump(),
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            today_tasks=today_tasks,
            week_tasks=week_tasks,
        )

    async def find_by_id(self, id: str) -> UserDto:
        user = await self.user_repository.find_by_id(id)
        return self._to_dto(user)
    
    async def find_by_email(self, email: str) -> UserDto:
        user = await self.user_repository.find_by_email(email)
        return self._to_dto(user)
    
    async def update(self, id: str, dto: UpdateUserDto) -> UserDto:
        user = await self.user_repository.update(id, dto)
        return self._to_dto(user)
    
    async def delete(self, id) -> str:
        await self.user_repository.delete(id)
        return id


