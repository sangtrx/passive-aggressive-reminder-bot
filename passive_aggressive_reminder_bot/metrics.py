"""Lightweight Prometheus metrics helpers with safe optional import.

Provides helpers that return metric objects when prometheus_client is
available, otherwise returns None-compatible stubs.
"""
from __future__ import annotations

from typing import Any

try:
    from prometheus_client import Counter, Histogram
except Exception:  # pragma: no cover - optional dependency
    Counter = None  # type: ignore
    Histogram = None  # type: ignore


def make_counter(name: str, description: str) -> Any:
    if Counter:
        return Counter(name, description)

    class _Noop:
        def inc(self, _=1):
            return None

    return _Noop()


def make_histogram(name: str, description: str) -> Any:
    if Histogram:
        return Histogram(name, description)

    class _Noop:
        def observe(self, _):
            return None

    return _Noop()
