"""Alembic env for SQLModel (async) autogenerate migrations.

Set `DATABASE_URL` environment variable (e.g. sqlite+aiosqlite:///./enterprise.db)
before running alembic commands.
"""
from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection

from alembic import context

from sqlmodel import SQLModel

# this is the Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
from passive_aggressive_reminder_bot.async_storage import SQLModel as _SQLModel  # noqa: F401

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    raise RuntimeError("offline mode not supported in this template")


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    from sqlalchemy.ext.asyncio import create_async_engine

    url = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./enterprise.db")
    connectable = create_async_engine(url, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
