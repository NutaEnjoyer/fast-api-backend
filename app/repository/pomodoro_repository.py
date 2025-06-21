"""
Pomodoro repository module for pomodoro session and round management.

This module contains the PomodoroRepository class which handles all database
operations related to pomodoro sessions and rounds, including session creation,
round management, and pomodoro timer functionality.
"""

from datetime import datetime, time
from sqlalchemy import delete, select, and_
from sqlalchemy.orm import selectinload
from app.core.database import PomodoroRoundOrm, PomodoroSessionOrm
from app.dto.pomodoro_dto import PomodoroRoundDto, PomodoroSessionDto
from app.repository.base_repository import BaseRepository
from app.repository.user_repository import UserRepository


class PomodoroRepository(BaseRepository):
    """
    Repository class for pomodoro session and round management.

    This class provides methods for creating and managing pomodoro sessions,
    handling pomodoro rounds, and tracking pomodoro timer functionality.
    """

    user_repository = UserRepository()

    async def get_today_session(self, user_id: str) -> PomodoroSessionOrm | None:
        """
        Get today's pomodoro session for a user.

        Args:
            user_id: ID of the user

        Returns:
            Today's pomodoro session if exists, None otherwise
        """
        async with self.session() as session:
            query = (
                select(PomodoroSessionOrm)
                .options(selectinload(PomodoroSessionOrm.rounds))
                .order_by(PomodoroSessionOrm.id.asc())
                .where(
                    and_(
                        PomodoroSessionOrm.user_id == user_id,
                        PomodoroSessionOrm.created_at
                        >= datetime.combine(datetime.today().date(), time.min),
                    )
                )
            )
            result = await session.execute(query)
            pomodoro_session = result.scalars().first()
            return pomodoro_session

    async def create(self, user_id: str) -> PomodoroSessionOrm:
        """
        Create a new pomodoro session for a user.

        If a session for today already exists, returns the existing session.
        Otherwise, creates a new session with the appropriate number of rounds
        based on the user's interval count settings.

        Args:
            user_id: ID of the user

        Returns:
            Created or existing pomodoro session

        Raises:
            ValueError: If user is not found
        """
        today_session = await self.get_today_session(user_id)
        if today_session:
            return today_session

        async with self.session() as session:
            user = await self.user_repository.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            pomodoro_session = PomodoroSessionOrm(user_id=user_id)
            session.add(pomodoro_session)

            await session.flush()

            interval_count = user.interval_count or 7  # default value
            for i in range(interval_count):
                pomodoro_session.rounds.append(
                    PomodoroRoundOrm(pomodoro_session_id=pomodoro_session.id)
                )
            await session.flush()
            await session.commit()
            await session.refresh(pomodoro_session)

            return pomodoro_session

    async def update_session(
        self, user_id: str, session_id: str, data: PomodoroSessionDto
    ) -> PomodoroSessionOrm:
        """
        Update a pomodoro session.

        Args:
            user_id: ID of the user who owns the session
            session_id: ID of the pomodoro session
            data: Updated session data

        Returns:
            Updated pomodoro session object

        Raises:
            ValueError: If session with the specified ID is not found
        """
        async with self.session() as session:
            query = select(PomodoroSessionOrm).where(
                and_(
                    PomodoroSessionOrm.id == session_id,
                    PomodoroSessionOrm.user_id == user_id,
                )
            )
            result = await session.execute(query)
            pomodoro_session = result.scalars().first()

            if not pomodoro_session:
                raise ValueError(f"Pomodoro session with id {session_id} not found")

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(pomodoro_session, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(pomodoro_session)
            return pomodoro_session

    async def update_round(
        self, round_id: str, data: PomodoroRoundDto
    ) -> PomodoroRoundOrm:
        """
        Update a pomodoro round.

        Args:
            round_id: ID of the pomodoro round
            data: Updated round data

        Returns:
            Updated pomodoro round object

        Raises:
            ValueError: If round with the specified ID is not found
        """
        async with self.session() as session:
            query = select(PomodoroRoundOrm).where(PomodoroRoundOrm.id == round_id)
            result = await session.execute(query)
            pomodoro_round = result.scalars().first()

            if not pomodoro_round:
                raise ValueError(f"Pomodoro round with id {round_id} not found")

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(pomodoro_round, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(pomodoro_round)
            return pomodoro_round

    async def delete_round(self, user_id: str, session_id: str, round_id: str) -> None:
        """
        Delete a pomodoro round.

        Args:
            user_id: ID of the user who owns the session
            session_id: ID of the pomodoro session
            round_id: ID of the pomodoro round to delete

        Note:
            This operation is irreversible and will permanently remove the round.
        """
        async with self.session() as session:
            query = delete(PomodoroRoundOrm).where(
                and_(
                    PomodoroRoundOrm.id == round_id,
                    PomodoroRoundOrm.pomodoro_session_id == session_id,
                    PomodoroRoundOrm.pomodoro_session.has(user_id=user_id),
                )
            )
            await session.execute(query)
            await session.commit()

    async def delete_session(self, user_id: str, session_id: str) -> None:
        """
        Delete a pomodoro session and all its rounds.

        Args:
            user_id: ID of the user who owns the session
            session_id: ID of the pomodoro session to delete

        Note:
            This operation is irreversible and will permanently remove the session
            and all associated rounds.
        """
        async with self.session() as session:
            query = delete(PomodoroSessionOrm).where(
                and_(
                    PomodoroSessionOrm.id == session_id,
                    PomodoroSessionOrm.user_id == user_id,
                )
            )
            query_2 = delete(PomodoroRoundOrm).where(
                and_(
                    PomodoroRoundOrm.pomodoro_session_id == session_id,
                    PomodoroRoundOrm.pomodoro_session.has(user_id=user_id),
                )
            )
            await session.execute(query_2)
            await session.execute(query)
            await session.commit()
