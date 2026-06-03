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
        self.index: set[str] = set()

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
        self.index.add(key)

    async def delete(self, key: str) -> int:
        if key in self.store:
            del self.store[key]
            self.index.discard(key)
            return 1
        return 0

    async def delete_pattern(self, pattern: str) -> int:
        # simple glob-like pattern using fnmatch
        import fnmatch

        keys = [k for k in list(self.index) if fnmatch.fnmatch(k, pattern)]
        for k in keys:
            self.store.pop(k, None)
            self.index.discard(k)
        return len(keys)


class RedisCache:
    def __init__(self, client):
        self._client = client
        self._index_key = "parb:cache_keys"

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
        # track the key in a Redis set for safe server-side listing without KEYS
        try:
            await self._client.sadd(self._index_key, key)
        except Exception:
            pass

    async def delete(self, key: str) -> int:
        res = await self._client.delete(key)
        try:
            return int(res)
        except Exception:
            return 0
        finally:
            try:
                await self._client.srem(self._index_key, key)
            except Exception:
                pass

    async def delete_pattern(self, pattern: str) -> int:
        # use a tracked Redis set to avoid KEYS which is unsafe at scale
        try:
            members = await self._client.smembers(self._index_key)
        except Exception:
            members = []
        import fnmatch

        to_delete = [m for m in members if fnmatch.fnmatch(m, pattern)]
        if not to_delete:
            return 0
        # delete keys and remove from index
        await self._client.delete(*to_delete)
        await self._client.srem(self._index_key, *to_delete)
        return len(to_delete)

    async def stats(self) -> dict[str, int]:
        try:
            size = await self._client.scard(self._index_key)
            return {"keys": int(size)}
        except Exception:
            return {"keys": 0}


async def make_cache(redis_url: str | None = None):
    if aioredis and redis_url:
        client = await aioredis.from_url(redis_url)
        return RedisCache(client)
    return SimpleInMemoryCache()
