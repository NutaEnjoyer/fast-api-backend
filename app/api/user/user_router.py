"""
User API router module.

This module provides user-related API endpoints including
profile management, user preferences, and account operations
with proper authentication and validation.
"""

from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies.auth import get_current_user
from app.dto.user_dto import GetUserDto, ResponseUserDto, UpdateUserDto
from app.repository.user_repository import UserRepository
from app.services.user_service import UserService


# User API router with prefix and tags
router = APIRouter(
    prefix="/user",
    tags=["User Management"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "User not found"},
        422: {"description": "Validation error"},
    },
)


def get_user_service() -> UserService:
    """
    Dependency injection for UserService.

    Creates and returns a UserService instance with
    a UserRepository dependency.

    Returns:
        UserService: Configured user service instance
    """
    repository = UserRepository()
    return UserService(repository)


@router.get(
    "",
    response_model=GetUserDto,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve the current authenticated user's profile with task statistics",
)
async def get_me(
    user_id: str = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> GetUserDto:
    """
    Get current user profile with statistics.

    Retrieves the authenticated user's profile information
    including personal data, pomodoro preferences, and
    aggregated task statistics.

    Args:
        user_id: Current user ID from JWT token
        service: User service dependency

    Returns:
        GetUserDto: User profile with task statistics

    Raises:
        HTTPException: If user not found or unauthorized
    """
    try:
        user = await service.get_me(user_id)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile",
        )


@router.put(
    "",
    response_model=ResponseUserDto,
    status_code=status.HTTP_200_OK,
    summary="Update user profile",
    description="Update the current authenticated user's profile and preferences",
)
async def update_user(
    dto: UpdateUserDto,
    user_id: str = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> ResponseUserDto:
    """
    Update current user profile.

    Updates the authenticated user's profile information
    including personal data and pomodoro preferences.
    All fields are optional for partial updates.

    Args:
        dto: User update data transfer object
        user_id: Current user ID from JWT token
        service: User service dependency

    Returns:
        ResponseUserDto: Updated user profile

    Raises:
        HTTPException: If user not found or update fails
    """
    try:
        user = await service.update(user_id, dto)
        return ResponseUserDto.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile",
        )
