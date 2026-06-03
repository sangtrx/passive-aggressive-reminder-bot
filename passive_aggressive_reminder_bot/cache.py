"""Caching helpers with aioredis fallback to in-memory cache."""
from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Optional

try:
    import aioredis
except Exception:  # pragma: no cover - optional dependency
    aioredis = None  # type: ignore


class SimpleInMemoryCache:
    def __init__(self):
        self.store: dict[str, tuple[float, Any]] = {}

    async def get(self, key: str):
        v = self.store.get(key)
        if not v:
            return None
        expire, val = v
        if expire and time.time() > expire:
            del self.store[key]
            return None
        return val

    async def set(self, key: str, value: Any, ttl: int | None = None):
        expire = time.time() + ttl if ttl else 0
        self.store[key] = (expire, value)


class RedisCache:
    def __init__(self, client):
        self._client = client

    async def get(self, key: str):
        v = await self._client.get(key)
        if v is None:
            return None
        # aioredis may return bytes; decode to str when appropriate
        if isinstance(v, (bytes, bytearray)):
            try:
                return v.decode()
            except Exception:
                return v
        return v

    async def set(self, key: str, value: Any, ttl: int | None = None):
        if ttl:
            # aioredis expects ex for TTL in seconds
            await self._client.set(key, value, ex=ttl)
        else:
            await self._client.set(key, value)


async def make_cache(redis_url: str | None = None):
    if aioredis and redis_url:
        client = await aioredis.from_url(redis_url)
        return RedisCache(client)
    return SimpleInMemoryCache()
