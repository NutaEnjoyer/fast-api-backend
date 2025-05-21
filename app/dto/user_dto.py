from pydantic import BaseModel

from app.dto.base_dto import BaseDto
from app.dto.response_dto import ResponseDto


class UserDto(BaseDto):
    email: str 
    name: str | None = None
    work_interval: int 
    break_interval: int 
    interval_count : int 

class UpdateUserDto(BaseModel):
    email: str | None = None
    password: str | None = None
    name: str | None = None
    work_interval: int | None = None
    break_interval: int | None = None
    interval_count : int | None = None

class GetUserDto(UserDto):
    total_tasks: int
    completed_tasks: int
    today_tasks: int
    week_tasks: int

class ResponseUserDto(UserDto):
    ...
