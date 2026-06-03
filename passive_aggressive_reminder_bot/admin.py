"""Tiny admin helpers for enterprise operations."""
from __future__ import annotations

from typing import Optional


def check_enterprise_key(provided: Optional[str], expected: Optional[str]) -> bool:
    """Simple check for an enterprise API key. In real deployments this should
    use a secure secret store; this helper centralizes the logic so it can be
    swapped later.
    """
    if not expected:
        return True
    return bool(provided) and provided == expected
