from typing import Type, TypeVar
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseService: 
    def _to_dto(self, dto_class: Type[T], data: dict) -> T:
        return dto_class.model_validate(data)
    