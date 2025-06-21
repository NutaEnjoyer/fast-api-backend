"""
Database configuration and models module.

This module provides SQLAlchemy async database configuration,
base models, and all ORM models for the application including
users, tasks, pomodoro sessions, and time blocks.
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.core.configs import DATABASE_URL

# Database engine configuration with improved settings
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries for debugging
    pool_pre_ping=True,  # Validate connections before use
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Maximum overflow connections
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Session factory for database operations
new_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class Model(DeclarativeBase):
    """
    Base declarative model for SQLAlchemy.

    This class serves as the foundation for all ORM models
    in the application using SQLAlchemy 2.0 style.
    """

    pass


class BaseModel(Model):
    """
    Abstract base model with common fields.

    Provides common fields like id, created_at, and updated_at
    that are shared across all models in the application.
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4()), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # Add timezone support
        default=datetime.now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # Add timezone support
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )


class UserOrm(BaseModel):
    """
    User model representing application users.

    Stores user authentication data, preferences, and relationships
    to other entities like tasks, time blocks, and pomodoro sessions.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Pomodoro preferences with validation
    work_interval: Mapped[int | None] = mapped_column(default=50)
    break_interval: Mapped[int | None] = mapped_column(default=10)
    interval_count: Mapped[int | None] = mapped_column(default=7)

    # Add constraints for pomodoro preferences
    __table_args__ = (
        CheckConstraint(
            "work_interval > 0 AND work_interval <= 120", name="work_interval_check"
        ),
        CheckConstraint(
            "break_interval > 0 AND break_interval <= 60", name="break_interval_check"
        ),
        CheckConstraint(
            "interval_count > 0 AND interval_count <= 20", name="interval_count_check"
        ),
    )

    # Relationships
    tasks: Mapped[list["TaskOrm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",  # Delete tasks when user is deleted
    )
    time_blocks: Mapped[list["TimeBlockOrm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",  # Delete time blocks when user is deleted
    )
    pomodoro_sessions: Mapped[list["PomodoroSessionOrm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",  # Delete sessions when user is deleted
    )


class TaskOrm(BaseModel):
    """
    Task model representing user tasks.

    Stores task information including title, description, priority,
    completion status, and relationship to the user who owns it.
    """

    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    priority: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Foreign key relationship
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped["UserOrm"] = relationship(back_populates="tasks")

    __table_args__ = (
        Index("idx_tasks_user_completed", "user_id", "is_completed"),
        Index("idx_tasks_priority", "priority"),
        CheckConstraint("priority IN ('low', 'medium', 'high')", name="priority_check"),
    )


class PomodoroSessionOrm(BaseModel):
    """
    Pomodoro session model representing a complete pomodoro session.

    A pomodoro session consists of multiple rounds and tracks
    the overall completion status of the session.
    """

    __tablename__ = "pomodoro_sessions"

    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Foreign key relationship
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped["UserOrm"] = relationship(back_populates="pomodoro_sessions")

    # Relationship to pomodoro rounds
    rounds: Mapped[list["PomodoroRoundOrm"]] = relationship(
        back_populates="pomodoro_session",
        cascade="all, delete-orphan",  # Delete rounds when session is deleted
    )
    __table_args__ = (
        Index("idx_pomodoro_sessions_user_completed", "user_id", "is_completed"),
    )


class PomodoroRoundOrm(BaseModel):
    """
    Pomodoro round model representing individual work/break intervals.

    Each round represents a single work or break period within
    a pomodoro session with its duration and completion status.
    """

    __tablename__ = "pomodoro_rounds"

    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    totalSeconds: Mapped[int] = mapped_column(nullable=False)

    # Foreign key relationship
    pomodoro_session_id: Mapped[str] = mapped_column(
        ForeignKey("pomodoro_sessions.id"), nullable=False, index=True
    )
    pomodoro_session: Mapped["PomodoroSessionOrm"] = relationship(
        back_populates="rounds"
    )

    # Add indexes and constraints for better query performance
    __table_args__ = (
        Index(
            "idx_pomodoro_rounds_session_completed",
            "pomodoro_session_id",
            "is_completed",
        ),
        CheckConstraint(
            "totalSeconds > 0 AND totalSeconds <= 3600", name="totalSeconds_check"
        ),
    )


class TimeBlockOrm(BaseModel):
    """
    Time block model representing scheduled time periods.

    Represents user-defined time blocks with custom names,
    colors, durations, and ordering for time management.
    """

    __tablename__ = "time_blocks"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(
        String(7), nullable=True, default=None  # Hex color code length (#RRGGBB)
    )
    duration: Mapped[int] = mapped_column(nullable=False)
    order: Mapped[int] = mapped_column(default=1, nullable=False)

    # Foreign key relationship
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped["UserOrm"] = relationship(back_populates="time_blocks")

    # Add indexes and constraints for better query performance
    __table_args__ = (
        Index("idx_time_blocks_user_order", "user_id", "order"),
        CheckConstraint(
            "duration > 0 AND duration <= 1440", name="duration_check"
        ),  # 1 minute to 24 hours
        CheckConstraint("order > 0", name="order_check"),
    )


async def create_tables():
    """
    Create all database tables.

    This function creates all tables defined in the models
    if they don't already exist. Useful for initial setup
    and development environments.

    Example:
        ```python
        await create_tables()
        ```
    """
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    """
    Delete all database tables.

    This function drops all tables defined in the models.
    Use with caution as this will permanently delete all data.
    Primarily used for testing and development cleanup.

    Example:
        ```python
        await delete_tables()
        ```
    """
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
