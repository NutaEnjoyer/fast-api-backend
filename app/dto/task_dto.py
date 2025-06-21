from pydantic import BaseModel
from enum import Enum

from app.dto.base_dto import BaseDto
from app.dto.response_dto import ResponseDto


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreateTaskDto(BaseModel):
    title: str
    description: str | None = None
    priority: Priority | None = None
    is_completed: bool = False


class TaskDto(CreateTaskDto, BaseDto):
    user_id: str


class ListTaskResponseDto(ResponseDto):
    tasks: list[TaskDto]


class TaskResponseDto(ResponseDto):
    task: TaskDto


class UpdateTaskDto(CreateTaskDto):
    title: str | None = None


class DeleteTaskResponseDto(ResponseDto):
    id: str
