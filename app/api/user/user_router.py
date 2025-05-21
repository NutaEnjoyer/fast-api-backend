from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dto.user_dto import ResponseUserDto, UpdateUserDto
from app.repository.user_repository import UserRepository
from app.services.user_service import UserService


router = APIRouter(prefix="/user", tags=["user"])

def get_user_service() -> UserService:
    repository = UserRepository()
    return UserService(repository)

@router.get("", response_model=ResponseUserDto, status_code=status.HTTP_200_OK)
async def get_me(
        user_id: str = Depends(get_current_user),
        service: UserService = Depends(get_user_service)
) -> ResponseUserDto:
    user = await service.find_by_id(user_id)
    return user

@router.put("", response_model=ResponseUserDto, status_code=status.HTTP_200_OK)
async def update_user(
    dto: UpdateUserDto,
    user_id: str = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> ResponseUserDto:
    user = await service.update(user_id, dto)
    return user
