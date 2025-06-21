from datetime import datetime
import os
from typing import List
from uuid import uuid4
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.core.configs import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class BaseModel(Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )


class TaskOrm(BaseModel):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str | None]
    priority: Mapped[str | None]
    is_completed: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserOrm"] = relationship(back_populates="tasks")


class UserOrm(BaseModel):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    name: Mapped[str | None]

    work_interval: Mapped[int | None] = mapped_column(default=50)
    break_interval: Mapped[int | None] = mapped_column(default=10)
    interval_count: Mapped[int | None] = mapped_column(default=7)

    tasks: Mapped[list["TaskOrm"]] = relationship(back_populates="user")
    time_blocks: Mapped[list["TimeBlockOrm"]] = relationship(back_populates="user")
    pomodoro_sessions: Mapped[list["PomodoroSessionOrm"]] = relationship(
        back_populates="user"
    )


class PomodoroSessionOrm(BaseModel):
    __tablename__ = "pomodoro_sessions"

    is_completed: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserOrm"] = relationship(back_populates="pomodoro_sessions")

    rounds: Mapped[list["PomodoroRoundOrm"]] = relationship(
        back_populates="pomodoro_session"
    )


class PomodoroRoundOrm(BaseModel):
    __tablename__ = "pomodoro_rounds"

    is_completed: Mapped[bool] = mapped_column(default=False)
    totalSeconds: Mapped[int]

    pomodoro_session_id: Mapped[str] = mapped_column(
        ForeignKey("pomodoro_sessions.id"), nullable=False
    )
    pomodoro_session: Mapped["PomodoroSessionOrm"] = relationship(
        back_populates="rounds"
    )


class TimeBlockOrm(BaseModel):
    __tablename__ = "time_blocks"

    name: Mapped[str]
    color: Mapped[str] = mapped_column(nullable=True, default=None)
    duration: Mapped[int]
    order: Mapped[int] = mapped_column(default=1)

    user: Mapped["UserOrm"] = relationship(back_populates="time_blocks")
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
