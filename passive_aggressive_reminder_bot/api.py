"""Lightweight FastAPI integration for enterprise deployments.

This module exposes a factory `create_app()` which builds a FastAPI app with
optional caching and Prometheus metrics. It defers importing FastAPI until
runtime so the package can be used without the enterprise dependencies.
"""
from __future__ import annotations

from typing import Any


def create_app() -> Any:
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import ORJSONResponse, PlainTextResponse
        from fastapi.concurrency import run_in_threadpool
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("FastAPI is not installed; install requirements-enterprise.txt") from exc

    # Optional deps
    try:
        from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
    except Exception:  # pragma: no cover - optional
        Counter = Histogram = None
        generate_latest = None
        CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"

    from pydantic import BaseModel

    from .core import generate_reminder
    from .cache import make_cache

    app = FastAPI(title="Passive-Aggressive Reminder Bot API")

    REQUEST_COUNT = Counter("parb_requests_total", "Total requests") if Counter else None
    REQUEST_LATENCY = Histogram("parb_request_latency_seconds", "Request latency") if Histogram else None


    class RemindRequest(BaseModel):
        message: str
        spice: int | None = None
        seed: int | None = None
        intent: str = "nudge"
        profile: str | None = None


    @app.on_event("startup")
    async def _startup():
        # initialize optional cache
        app.state.cache = await make_cache(None)


    @app.post("/remind", response_class=ORJSONResponse)
    async def remind(req: RemindRequest):
        if REQUEST_COUNT:
            REQUEST_COUNT.inc()
        start = None
        if REQUEST_LATENCY:
            start = REQUEST_LATENCY.time()

        try:
            # run CPU-bound generate_reminder in threadpool
            class R:  # lightweight request-like object
                pass

            r = R()
            r.message = req.message
            r.spice = req.spice or 2
            r.seed = req.seed
            r.intent = req.intent
            r.profile = req.profile

            # cache key by message+spice+intent+profile
            key = f"reminder:{req.intent}:{req.spice or 2}:{req.message}:{req.profile}"
            cached = await app.state.cache.get(key)
            if cached:
                reminder = cached
            else:
                reminder = await run_in_threadpool(generate_reminder, r)
                await app.state.cache.set(key, reminder, ttl=60)

            return {"reminder": reminder}
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            if REQUEST_LATENCY and start:
                start.observe()


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


    if generate_latest:
        @app.get("/metrics")
        def _metrics():
            return ORJSONResponse(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app
