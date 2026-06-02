from __future__ import annotations

import random

from .data import TAILS
from .models import ReminderRequest


def generate_reminder(request: ReminderRequest) -> str:
    rng = random.Random(request.seed)
    base = f"Just a gentle reminder to {request.message}."
    tail = rng.choice(TAILS[request.spice])
    return f"{base} {tail}"
