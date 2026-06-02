from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReminderRequest:
    message: str
    spice: int = 2
    seed: int | None = None
