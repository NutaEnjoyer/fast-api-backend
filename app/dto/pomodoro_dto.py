from pydantic import BaseModel

from app.dto.base_dto import BaseDto


class UpdatePomodoroSessionDto(BaseModel):
    is_completed: bool | None = None


class UpdatePomodoroRoundDto(BaseModel):
    total_seconds: int
    is_completed: bool | None = None
 

class PomodoroSessionDto(BaseDto):
    is_completed: bool


class PomodoroRoundDto(BaseDto):
    total_seconds: int | None
    is_completed: bool | None

