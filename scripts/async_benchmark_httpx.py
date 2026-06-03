"""Async HTTP benchmark for the /remind endpoint using httpx.

Sends concurrent requests and reports ops/sec.
"""
from __future__ import annotations

import asyncio
import time
import httpx


async def worker(client: httpx.AsyncClient, q: asyncio.Queue):
    while True:
        payload = await q.get()
        if payload is None:
            break
        await client.post('http://127.0.0.1:8000/remind', json=payload)
        q.task_done()


async def run(total: int = 1000, concurrency: int = 50):
    q = asyncio.Queue()
    async with httpx.AsyncClient(timeout=10.0) as client:
        workers = [asyncio.create_task(worker(client, q)) for _ in range(concurrency)]
        start = time.perf_counter()
        for _ in range(total):
            await q.put({'message': 'benchmark', 'spice': 2})
        await q.join()
        elapsed = time.perf_counter() - start
        for _ in range(concurrency):
            await q.put(None)
        await asyncio.gather(*workers)
    print(f"{total} requests in {elapsed:.2f}s -> {total/elapsed:.0f} req/s")


if __name__ == '__main__':
    asyncio.run(run(1000, 50))