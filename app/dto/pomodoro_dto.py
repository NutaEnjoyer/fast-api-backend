"""
Pomodoro DTO (Data Transfer Object) module.

This module provides DTOs for pomodoro-related operations including
session management, round tracking, and data validation for time management.
"""

from app.dto.base_dto import BaseDto, BaseModelDto


class UpdatePomodoroSessionDto(BaseModelDto):
    """
    DTO for updating pomodoro sessions.

    Allows updating session completion status.
    """

    is_completed: bool | None = None


class UpdatePomodoroRoundDto(BaseModelDto):
    """
    DTO for updating pomodoro rounds.

    Allows updating round completion status and duration.
    """

    total_seconds: int
    is_completed: bool | None = None


class PomodoroSessionDto(BaseDto):
    """
    Complete pomodoro session DTO.

    Contains session data with base fields and
    relationship to user and rounds.
    """

    is_completed: bool


class PomodoroRoundDto(BaseDto):
    """
    Complete pomodoro round DTO.

    Contains round data with base fields and
    relationship to pomodoro session.
    """

    total_seconds: int | None
    is_completed: bool | None
