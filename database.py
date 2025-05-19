from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import aiosqlite


engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db",
    # "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapiplanner",
    # echo=True,
    # pool_pre_ping=True
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class BaseModel(Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class TaskOrm(BaseModel):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str | None]
    priority: Mapped[str | None]
    is_completed: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[str | None]



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
