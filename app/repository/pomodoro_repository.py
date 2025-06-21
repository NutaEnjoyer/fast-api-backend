

from datetime import datetime, time
from sqlalchemy import delete, select, and_
from app.core.database import PomodoroRoundOrm, PomodoroSessionOrm
from app.dto.pomodoro_dto import PomodoroRoundDto, PomodoroSessionDto
from app.repository.base_repository import BaseRepository
from app.repository.user_repository import UserRepository


class PomodoroRepository(BaseRepository):
    user_repository = UserRepository()


    async def get_today_session(self, user_id: str) -> PomodoroSessionOrm | None:
        async with self.session() as session:
            query = (select(PomodoroSessionOrm)
                                .selectinload(PomodoroSessionOrm.rounds)
                                .order_by(PomodoroSessionOrm.rounds.property.mapper.class_.id.asc())
                                .where(
                                    and_(
                                        PomodoroSessionOrm.user_id == user_id,
                                        PomodoroSessionOrm.created_at >= datetime.combine(datetime.today().date(), time.min)
                                        )
                                    )
                                )
            result = await session.execute(query)
            pomodoro_session = result.scalars().first()
            return pomodoro_session
    

    async def create(self, user_id: str) -> PomodoroSessionOrm:
        today_session = await self.get_today_session(user_id)
        if  today_session: return today_session

        async with self.session() as session:
            user = await self.user_repository.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            pomodoro_session = PomodoroSessionOrm(user_id=user_id)
            session.add(pomodoro_session)
            
            await session.flush()

            for i in range(user.interval_count):
                pomodoro_session.rounds.append(PomodoroRoundOrm(pomodoro_session_id=pomodoro_session.id))
            await session.flush()
            await session.commit()
            await session.refresh(pomodoro_session)

            return pomodoro_session
    
    async def update_session(
            self,
            user_id: str,
            session_id: str,
            data: PomodoroSessionDto
    ) -> PomodoroSessionOrm:
        async with self.session() as session:
            query = (select(PomodoroSessionOrm)
                                .where(
                                    and_(
                                        PomodoroSessionOrm.id == session_id,
                                        PomodoroSessionOrm.user_id == user_id
                                        )
                                    )
                                )
            result = await session.execute(query)
            pomodoro_session = result.scalars().first()
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(pomodoro_session, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(pomodoro_session)
            return pomodoro_session


    async def update_round(
            self,
            round_id: str,
            data: PomodoroRoundDto
            ) -> PomodoroRoundOrm:
        async with self.session() as session:
            query = (select(PomodoroRoundOrm)
                                .where(PomodoroRoundOrm.id == round_id)
                                )
            result = await session.execute(query)
            pomodoro_round = result.scalars().first()
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(pomodoro_round, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(pomodoro_round)
            return pomodoro_round


    async def delete_round(self, user_id: str, session_id: str, round_id: str) -> None:
        async with self.session() as session:
            query = delete(PomodoroRoundOrm).where(
                and_(
                    PomodoroRoundOrm.id == round_id,
                    PomodoroRoundOrm.pomodoro_session_id == session_id,
                    PomodoroRoundOrm.pomodoro_session.has(user_id=user_id)
                )
            )
            await session.execute(query)
            await session.commit()

    async def delete_session(self, user_id: str, session_id: str) -> None:
        async with self.session() as session:
            query = delete(PomodoroSessionOrm).where(
                and_(
                    PomodoroSessionOrm.id == session_id,
                    PomodoroSessionOrm.user_id == user_id
                )
            )
            query_2 = delete(PomodoroRoundOrm).where(
                and_(
                    PomodoroRoundOrm.pomodoro_session_id == session_id,
                    PomodoroRoundOrm.pomodoro_session.has(user_id=user_id)
                )
            )
            await session.execute(query_2)
            await session.execute(query)
            await session.commit()
            