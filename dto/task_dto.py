from pydantic import BaseModel
from enum import Enum

from dto.base_dto import BaseDto


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreateTaskDto(BaseModel):
    title: str 
    description: str | None = None
    priority: Priority | None = None
    is_completed: bool = False

    user_id: str | None = None


class TaskDto(CreateTaskDto, BaseDto):
    pass


class CreateTaskResponseDto(BaseModel):
    ok: bool = True
    task_id: str
    
class TaskResponseDto(BaseModel):
    ok: bool = True
    tasks: list[TaskDto]