from __future__ import annotations

import random

from .data import INTENT_TEMPLATES, TAILS
from .models import Profile, ReminderRequest


def generate_reminder(request: ReminderRequest, profile: Profile | None = None) -> str:
    rng = random.Random(request.seed)
    templates = INTENT_TEMPLATES.get(request.intent, INTENT_TEMPLATES["nudge"])
    base = rng.choice(templates).format(message=request.message)
    tail = rng.choice(TAILS[request.spice])
    greeting = f"Hey {profile.display_name}," if profile else ""
    signoff = profile.signoff if profile else ""
    parts = [part for part in (greeting, base, tail) if part]
    if signoff:
        parts.append(f"— {signoff}")
    return " ".join(parts)
