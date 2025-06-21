"""
Pomodoro API router module.

This module provides pomodoro-related API endpoints including
session management, round tracking, and time management operations
with proper authentication and validation.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.dto.pomodoro_dto import PomodoroRoundDto, PomodoroSessionDto
from app.repository.pomodoro_repository import PomodoroRepository
from app.services.pomodoro_service import PomodoroService


# Pomodoro API router with prefix and tags
router = APIRouter(
    prefix="/pomodoro",
    tags=["Pomodoro Management"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Pomodoro session/round not found"},
        422: {"description": "Validation error"},
    },
)


def get_pomodoro_service() -> PomodoroService:
    """
    Dependency injection for PomodoroService.

    Creates and returns a PomodoroService instance with
    a PomodoroRepository dependency.

    Returns:
        PomodoroService: Configured pomodoro service instance
    """
    repository = PomodoroRepository()
    return PomodoroService(repository)


@router.post(
    "/",
    response_model=PomodoroSessionDto,
    status_code=status.HTTP_201_CREATED,
    summary="Create pomodoro session",
    description="Create a new pomodoro session for the authenticated user",
)
async def create_pomodoro(
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user),
) -> PomodoroSessionDto:
    """
    Create a new pomodoro session.

    Creates a new pomodoro session for the authenticated user
    with default settings and initial state.

    Args:
        service: Pomodoro service dependency
        current_user: Current user ID from JWT token

    Returns:
        PomodoroSessionDto: Created pomodoro session
    """
    pomodoro = await service.create(current_user)
    return pomodoro


@router.get(
    "/today",
    response_model=PomodoroSessionDto,
    status_code=status.HTTP_200_OK,
    summary="Get today's pomodoro session",
    description="Retrieve the pomodoro session for today for the authenticated user",
)
async def get_today_pomodoro(
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user),
) -> PomodoroSessionDto:
    """
    Get today's pomodoro session.

    Retrieves the pomodoro session for the current day
    belonging to the authenticated user.

    Args:
        service: Pomodoro service dependency
        current_user: Current user ID from JWT token

    Returns:
        PomodoroSessionDto: Today's pomodoro session
    """
    try:
        pomodoro = await service.get_today_pomodoro(current_user)
        return pomodoro
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve today's pomodoro session",
        )


@router.put(
    "/round/{round_id}",
    response_model=PomodoroRoundDto,
    status_code=status.HTTP_200_OK,
    summary="Update pomodoro round",
    description="Update a specific pomodoro round by its ID",
)
async def update_pomodoro_round(
    round_id: str,
    pomodoro_round_data: PomodoroRoundDto,
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user),
) -> PomodoroRoundDto:
    """
    Update a pomodoro round.

    Updates a specific pomodoro round with new data
    such as completion status and duration.

    Args:
        round_id: ID of the round to update
        pomodoro_round_data: Round update data
        service: Pomodoro service dependency
        current_user: Current user ID from JWT token

    Returns:
        PomodoroRoundDto: Updated pomodoro round
    """
    try:
        pomodoro_round = await service.update_pomodoro_round(
            round_id, pomodoro_round_data
        )
        return pomodoro_round
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update pomodoro round",
        )


@router.put(
    "/session/{session_id}",
    response_model=PomodoroSessionDto,
    status_code=status.HTTP_200_OK,
    summary="Update pomodoro session",
    description="Update a pomodoro session by its ID",
)
async def update_pomodoro_session(
    session_id: str,
    pomodoro_session_data: PomodoroSessionDto,
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user),
) -> PomodoroSessionDto:
    """
    Update a pomodoro session.

    Updates a pomodoro session with new data such as
    completion status and session information.

    Args:
        session_id: ID of the session to update
        pomodoro_session_data: Session update data
        service: Pomodoro service dependency
        current_user: Current user ID from JWT token

    Returns:
        PomodoroSessionDto: Updated pomodoro session
    """
    try:
        pomodoro_session = await service.update_pomodoro_session(
            current_user, session_id, pomodoro_session_data
        )
        return pomodoro_session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update pomodoro session",
        )


@router.delete(
    "/session/{session_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete pomodoro session",
    description="Delete a pomodoro session by its ID",
)
async def delete_pomodoro_session(
    session_id: str,
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user),
) -> dict:
    """
    Delete a pomodoro session.

    Permanently deletes a pomodoro session belonging to
    the authenticated user. This action cannot be undone.

    Args:
        session_id: ID of the session to delete
        service: Pomodoro service dependency
        current_user: Current user ID from JWT token

    Returns:
        dict: Confirmation of deletion with session ID
    """
    try:
        deleted_session_id = await service.delete_pomodoro_session(
            current_user, session_id
        )
        return {
            "id": deleted_session_id,
            "message": "Pomodoro session deleted successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete pomodoro session",
        )
