"""Lightweight FastAPI integration for enterprise deployments.

This module exposes a factory `create_app()` which builds a FastAPI app.
Importing this module does not require FastAPI to be installed; the import
error is deferred until `create_app()` is called.
"""
from __future__ import annotations

from typing import Any


def create_app() -> Any:
    """Create and return a FastAPI application instance.

    This defers importing FastAPI until runtime so the package can be used
    without installing the optional enterprise dependencies.
    """
    try:
        from fastapi import FastAPI
        from fastapi.responses import PlainTextResponse
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("FastAPI is not installed; install requirements-enterprise.txt") from exc

    app = FastAPI(title="Passive-Aggressive Reminder Bot API")


    @app.get("/health", response_class=PlainTextResponse)
    def _health() -> str:  # pragma: no cover - small endpoint
        return "ok"


    @app.get("/version", response_class=PlainTextResponse)
    def _version() -> str:
        try:
            from . import __version__

            return __version__
        except Exception:
            return "unknown"

    return app
