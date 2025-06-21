from contextlib import AbstractContextManager
from typing import TypeVar, Type, Callable

from sqlalchemy.orm import Session

from app.core.database import new_session
from app.core.database import BaseModel


TypeOrm =  TypeVar("TypeOrm", bound=BaseModel)

class BaseRepository:
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session = session

    