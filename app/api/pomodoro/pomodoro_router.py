from fastapi import APIRouter

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dto.pomodoro_dto import PomodoroRoundDto, PomodoroSessionDto
from app.repository.pomodoro_repository import PomodoroRepository
from app.services.pomodoro_service import PomodoroService


router = APIRouter(prefix="/pomodoro", tags=["pomodoro"])

def get_pomodoro_service() -> PomodoroService:
    repository = PomodoroRepository()
    return PomodoroService(repository)


@router.post("/")
async def create_pomodoro(
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user)
):
    pomodoro = await service.create(current_user)
    return pomodoro


@router.get("/today", status_code=status.HTTP_200_OK)
async def get_today_pomodoro(
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user)
) -> PomodoroSessionDto:
    pomodoro = await service.get_today_pomodoro(current_user)
    return pomodoro

@router.put('/round/{round_id}', status_code=status.HTTP_200_OK)
async def update_pomodoro_round(
    round_id: str,
    pomodoro_round: PomodoroRoundDto,
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user)
):
    pomodoro_round = await service.update_pomodoro_round(round_id, pomodoro_round)

@router.put('/session/{session_id}', status_code=status.HTTP_200_OK)
async def update_pomodoro_session(
    session_id: str,
    pomodoro_session: PomodoroSessionDto,
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user)
) -> PomodoroSessionDto: 
    pomodoro_session = await service.update_pomodoro_session(current_user, session_id, pomodoro_session)
    return pomodoro_session

@router.delete('/session/{session_id}', status_code=status.HTTP_200_OK)
async def delete_pomodoro_session(
    session_id: str,
    service: PomodoroService = Depends(get_pomodoro_service),
    current_user: str = Depends(get_current_user)
) -> str:
    session_id = await service.delete_pomodoro_session(current_user, session_id)
    return session_id
