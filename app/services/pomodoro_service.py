
from app.core.database import PomodoroRoundOrm, PomodoroSessionOrm
from app.dto.pomodoro_dto import PomodoroRoundDto, PomodoroSessionDto
from app.repository.base_repository import BaseRepository
from app.repository.pomodoro_repository import PomodoroRepository
from app.services.base_service import BaseService


class PomodoroService(BaseService):
    def __init__(self, pomodoro_repository: PomodoroRepository = PomodoroRepository()):
        self.pomodoro_repository = pomodoro_repository
    
    async def create(self, user_id: str) -> PomodoroSessionDto:
        pomodoro = await self.pomodoro_repository.create(user_id)
        return self._to_dto(PomodoroSessionDto, pomodoro)

    async def get_today_pomodoro(self, user_id: str) -> PomodoroSessionDto:
        pomodoro = await self.pomodoro_repository.get_today_session(user_id)
        return self._to_dto(PomodoroSessionDto, pomodoro)
    
    async def update_pomodoro_session(self, user_id: str, session_id: str, pomodoro_session: PomodoroSessionDto) -> PomodoroSessionDto:
        pomodoro_session = await self.pomodoro_repository.update_session(user_id, session_id, pomodoro_session)
        return self._to_dto(PomodoroSessionDto, pomodoro_session)
    
    async def update_pomodoro_round(self, round_id: str, pomodoro_round: PomodoroRoundDto) -> PomodoroRoundDto:
        pomodoro_round = await self.pomodoro_repository.update_round(round_id, pomodoro_round)
        return self._to_dto(PomodoroRoundDto, pomodoro_round)
    
    async def delete_pomodoro_session(self, user_id: str, session_id: str) -> str:
        await self.pomodoro_repository.delete_session(user_id, session_id)
        return session_id
    