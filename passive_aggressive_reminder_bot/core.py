"""Core reminder generation logic."""

from __future__ import annotations

import logging
import random

from .data import INTENT_TEMPLATES, TAILS
from functools import lru_cache
from .models import Profile, ReminderRequest
from .validation import validate_message, validate_spice

logger = logging.getLogger(__name__)


@lru_cache(maxsize=256)
def _render_template(intent: str, message: str, spice: int, seed: int | None, profile_name: str | None, signoff: str | None) -> str:
    rng = random.Random(seed)
    templates = INTENT_TEMPLATES.get(intent, INTENT_TEMPLATES["nudge"])
    base = rng.choice(templates).format(message=message)
    tail = rng.choice(TAILS[spice])
    greeting = f"Hey {profile_name}," if profile_name else ""
    parts = [part for part in (greeting, base, tail) if part]
    if signoff:
        parts.append(f"— {signoff}")
    return " ".join(parts)


def generate_reminder(request: ReminderRequest, profile: Profile | None = None) -> str:
    """Generate a reminder message based on the request and optional profile.
    
    Combines intent template, sass tail, and personalization elements to create
    a unique reminder message. Respects the random seed for reproducibility.
    
    Args:
        request: ReminderRequest containing message, spice, intent, seed, etc.
        profile: Optional Profile for personalization (display name, signoff)
        
    Returns:
        A formatted reminder message string
        
    Raises:
        ValueError: If validation fails
    """
    # Validate inputs
    validate_message(request.message)
    spice = validate_spice(request.spice)
    
    profile_name = profile.display_name if profile else None
    signoff = profile.signoff if profile else None
    message = _render_template(request.intent, request.message, spice, request.seed or 0, profile_name, signoff)
    logger.debug(
        f"Generated reminder: intent={request.intent}, spice={spice}, "
        f"profile={profile.name if profile else 'none'}"
    )
    return message
