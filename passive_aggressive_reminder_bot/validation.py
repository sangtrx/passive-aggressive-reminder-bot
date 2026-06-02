"""Input validation utilities."""

from __future__ import annotations

import re
from datetime import datetime

from .constants import MAX_SPICE, MIN_SPICE
from .exceptions import ValidationError


def validate_spice(spice: int) -> int:
    """Validate and return spice level (1-5).
    
    Args:
        spice: Spice level to validate
        
    Returns:
        Valid spice level
        
    Raises:
        ValidationError: If spice is out of valid range
    """
    if not isinstance(spice, int):
        raise ValidationError(f"Spice must be an integer, got {type(spice).__name__}")
    if not MIN_SPICE <= spice <= MAX_SPICE:
        raise ValidationError(f"Spice must be between {MIN_SPICE} and {MAX_SPICE}, got {spice}")
    return spice


def validate_profile_name(name: str) -> str:
    """Validate profile name format.
    
    Profile names should be alphanumeric with underscores and hyphens allowed.
    
    Args:
        name: Profile name to validate
        
    Returns:
        Validated profile name
        
    Raises:
        ValidationError: If name format is invalid
    """
    if not name:
        raise ValidationError("Profile name cannot be empty")
    if not re.match(r"^[a-zA-Z0-9_\-]+$", name):
        raise ValidationError(
            f"Profile name must contain only alphanumeric characters, underscores, and hyphens"
        )
    if len(name) > 50:
        raise ValidationError("Profile name must be 50 characters or less")
    return name


def validate_message(message: str) -> str:
    """Validate reminder message.
    
    Args:
        message: Message to validate
        
    Returns:
        Validated message
        
    Raises:
        ValidationError: If message is invalid
    """
    if not message:
        raise ValidationError("Message cannot be empty")
    if len(message) > 500:
        raise ValidationError("Message must be 500 characters or less")
    return message.strip()


def validate_datetime(dt_str: str) -> datetime:
    """Validate ISO format datetime string.
    
    Args:
        dt_str: ISO format datetime string
        
    Returns:
        Parsed datetime object
        
    Raises:
        ValidationError: If datetime format is invalid
    """
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError as e:
        raise ValidationError(f"Invalid datetime format (expected ISO 8601): {dt_str}") from e
