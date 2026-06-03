"""Simple benchmark harness for generate_reminder."""
from __future__ import annotations

import time
from passive_aggressive_reminder_bot.core import generate_reminder
from passive_aggressive_reminder_bot.models import ReminderRequest


def run(n: int = 10000):
    req = ReminderRequest(message="do the thing", spice=2, seed=42, intent="nudge")
    start = time.perf_counter()
    for _ in range(n):
        _ = generate_reminder(req)
    elapsed = time.perf_counter() - start
    print(f"Generated {n} reminders in {elapsed:.3f}s ({n/elapsed:.0f} ops/s)")


if __name__ == "__main__":
    run(10000)
