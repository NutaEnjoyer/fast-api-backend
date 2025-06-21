"""
User DTO (Data Transfer Object) module.

This module provides DTOs for user-related operations including
profile management, preferences, and data validation for user entities.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.dto.base_dto import BaseDto, BaseModelDto, alias_generator
from app.dto.response_dto import ResponseDto


class UserDto(BaseDto):
    """
    Complete user DTO with all fields.

    Contains user profile information, authentication data,
    and pomodoro preferences with base fields.
    """

    email: str
    name: str | None = None
    work_interval: int
    break_interval: int
    interval_count: int


class UpdateUserDto(BaseModelDto):
    """
    DTO for updating existing users.

    All fields are optional to allow partial updates
    of user profile and preferences.
    """

    email: str | None = None
    password: str | None = None
    name: str | None = None
    work_interval: int | None = None
    break_interval: int | None = None
    interval_count: int | None = None


class GetUserDto(UserDto):
    """
    Extended user DTO with task statistics.

    Includes user profile data plus aggregated task statistics
    for dashboard and analytics purposes.
    """

    total_tasks: int
    completed_tasks: int
    today_tasks: int
    week_tasks: int


class ResponseUserDto(UserDto):
    """
    Response DTO for user operations.

    Contains user data with success status.
    """

    pass
