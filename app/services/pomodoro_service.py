"""
Pomodoro service module for pomodoro session and round management.

This module contains the PomodoroService class which handles business logic
for pomodoro sessions and rounds, including session creation, round management,
and pomodoro timer functionality.
"""

from app.core.database import PomodoroRoundOrm, PomodoroSessionOrm
from app.dto.pomodoro_dto import PomodoroRoundDto, PomodoroSessionDto
from app.repository.base_repository import BaseRepository
from app.repository.pomodoro_repository import PomodoroRepository
from app.services.base_service import BaseService


class PomodoroService(BaseService):
    """
    Service class for pomodoro session and round management.

    This class handles business logic for pomodoro sessions and rounds,
    including session creation, round management, and pomodoro timer
    functionality. It acts as an intermediary between the API layer
    and the repository layer.
    """

    def __init__(self, pomodoro_repository: PomodoroRepository = PomodoroRepository()):
        """
        Initialize the pomodoro service.

        Args:
            pomodoro_repository: Repository for pomodoro operations
        """
        self.pomodoro_repository = pomodoro_repository

    async def create(self, user_id: str) -> PomodoroSessionDto:
        """
        Create a new pomodoro session for a user.

        Args:
            user_id: ID of the user

        Returns:
            Created pomodoro session DTO
        """
        pomodoro = await self.pomodoro_repository.create(user_id)
        return self._to_dto(PomodoroSessionDto, pomodoro)

    async def get_today_pomodoro(self, user_id: str) -> PomodoroSessionDto:
        """
        Get today's pomodoro session for a user.

        Args:
            user_id: ID of the user

        Returns:
            Today's pomodoro session DTO or None
        """
        pomodoro = await self.pomodoro_repository.get_today_session(user_id)
        return self._to_dto(PomodoroSessionDto, pomodoro)

    async def update_pomodoro_session(
        self, user_id: str, session_id: str, pomodoro_session: PomodoroSessionDto
    ) -> PomodoroSessionDto:
        """
        Update a pomodoro session.

        Args:
            user_id: ID of the user who owns the session
            session_id: ID of the pomodoro session
            pomodoro_session: Updated session data

        Returns:
            Updated pomodoro session DTO
        """
        updated_session = await self.pomodoro_repository.update_session(
            user_id, session_id, pomodoro_session
        )
        return self._to_dto(PomodoroSessionDto, updated_session)

    async def update_pomodoro_round(
        self, round_id: str, pomodoro_round: PomodoroRoundDto
    ) -> PomodoroRoundDto:
        """
        Update a pomodoro round.

        Args:
            round_id: ID of the pomodoro round
            pomodoro_round: Updated round data

        Returns:
            Updated pomodoro round DTO
        """
        updated_round = await self.pomodoro_repository.update_round(
            round_id, pomodoro_round
        )
        return self._to_dto(PomodoroRoundDto, updated_round)

    async def delete_pomodoro_session(self, user_id: str, session_id: str) -> str:
        """
        Delete a pomodoro session and all its rounds.

        Args:
            user_id: ID of the user who owns the session
            session_id: ID of the pomodoro session to delete

        Returns:
            ID of the deleted session
        """
        await self.pomodoro_repository.delete_session(user_id, session_id)
        return session_id
