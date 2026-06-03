"""Optional SQLAlchemy engine helper for enterprise deployments."""
from __future__ import annotations

from sqlalchemy import create_engine


def make_engine(url: str = 'sqlite:///reminder_bot_enterprise.db'):
    return create_engine(url, future=True)

