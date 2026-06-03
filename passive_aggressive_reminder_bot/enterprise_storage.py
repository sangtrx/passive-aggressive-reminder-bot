"""Optional SQLAlchemy-backed storage adapter for enterprise use.

This module defers importing SQLAlchemy until runtime to keep core usage
lightweight. It provides a helper to create an engine connected to a
SQLite database for deployments that prefer SQL over JSON files.
"""
from __future__ import annotations

from typing import Optional


def create_engine_sqlite(path: str | None = None):
    try:
        from sqlalchemy import create_engine
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("SQLAlchemy is not installed; install requirements-enterprise.txt") from exc

    db_url = f"sqlite:///{path or ':memory:'}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    return engine
