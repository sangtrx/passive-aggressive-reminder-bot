"""Async SQLModel storage helpers for enterprise deployments."""
from __future__ import annotations

from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.ext.asyncio.engine import create_async_engine
import asyncio


class ProfileModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    display_name: str
    pronouns: str
    signoff: str
    default_spice: int = 2


class ScheduledModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message: str
    spice: int
    intent: str
    channel: str
    profile: str | None
    due_at: str
    created_at: str
    status: str = "pending"


async def init_db(url: str = "sqlite+aiosqlite:///./enterprise.db") -> None:
    engine = create_async_engine(url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_schedules(async_engine, limit: int = 100) -> list[ScheduledModel]:
    async with AsyncSession(async_engine) as session:
        result = await session.exec(select(ScheduledModel).limit(limit))
        return result.all()
