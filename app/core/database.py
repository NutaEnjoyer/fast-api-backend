from datetime import datetime
import os
from uuid import uuid4
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.core.configs import Config


engine = create_async_engine(
    Config.get_env("DATABASE_URL"),
    echo=True,
    pool_pre_ping=True
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class BaseModel(Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


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
    # time_blocks = Mapped[list["TimeBlockOrm"]] = relationship(back_populates="user")
    # pomodoro_sessions = Mapped[list["PomodoroSessionOrm"]] = relationship(back_populates="user")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
