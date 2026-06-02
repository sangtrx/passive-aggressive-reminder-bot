"""Test configuration and fixtures."""

import pytest
from pathlib import Path
from passive_aggressive_reminder_bot.models import Profile, ReminderRequest


@pytest.fixture
def sample_profile() -> Profile:
    """Create a sample profile for testing."""
    return Profile(
        name="alex",
        display_name="Alex",
        pronouns="they/them",
        signoff="Thanks, Alex",
        default_spice=2,
    )


@pytest.fixture
def sample_request() -> ReminderRequest:
    """Create a sample reminder request for testing."""
    return ReminderRequest(
        message="update the roadmap",
        spice=2,
        seed=42,
        intent="nudge",
        profile=None,
        channel="plain",
    )
