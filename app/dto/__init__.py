"""
DTO (Data Transfer Object) package.

This package provides all DTOs for the application including
base DTOs, task DTOs, user DTOs, pomodoro DTOs, auth DTOs,
and response DTOs with comprehensive validation and documentation.
"""

# Base DTOs
from .base_dto import BaseDto, alias_generator

# Task DTOs
from .task_dto import (
    Priority,
    CreateTaskDto,
    TaskDto,
    UpdateTaskDto,
    ListTaskResponseDto,
    TaskResponseDto,
    DeleteTaskResponseDto,
)

# User DTOs
from .user_dto import (
    UserDto,
    UpdateUserDto,
    GetUserDto,
)

# Pomodoro DTOs
from .pomodoro_dto import (
    UpdatePomodoroSessionDto,
    PomodoroSessionDto,
    UpdatePomodoroRoundDto,
    PomodoroRoundDto,
)

# Auth DTOs
from .auth_dto import (
    AuthResponseDto,
    AuthDto,
)

# Response DTOs
from .response_dto import (
    ResponseDto,
)

__all__ = [
    # Base
    "BaseDto",
    "alias_generator",
    # Task
    "Priority",
    "CreateTaskDto",
    "TaskDto",
    "UpdateTaskDto",
    "ListTaskResponseDto",
    "TaskResponseDto",
    "DeleteTaskResponseDto",
    # User
    "UserDto",
    "UpdateUserDto",
    "GetUserDto",
    # Pomodoro
    "UpdatePomodoroSessionDto",
    "PomodoroSessionDto",
    "UpdatePomodoroRoundDto",
    "PomodoroRoundDto",
    # Auth
    "AuthResponseDto",
    "AuthDto",
    # Response
    "ResponseDto",
]
