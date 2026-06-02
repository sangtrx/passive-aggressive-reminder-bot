"""Tests for core reminder generation."""

import pytest
from passive_aggressive_reminder_bot.core import generate_reminder
from passive_aggressive_reminder_bot.models import Profile, ReminderRequest
from passive_aggressive_reminder_bot.validation import ValidationError


def test_generate_reminder_without_profile(sample_request):
    """Test generating a reminder without a profile."""
    reminder = generate_reminder(sample_request)
    assert isinstance(reminder, str)
    assert len(reminder) > 0
    assert "update the roadmap" in reminder


def test_generate_reminder_with_profile(sample_request, sample_profile):
    """Test generating a reminder with a profile."""
    reminder = generate_reminder(sample_request, profile=sample_profile)
    assert isinstance(reminder, str)
    assert "Alex" in reminder
    assert "Thanks, Alex" in reminder


def test_generate_reminder_with_seed(sample_request):
    """Test that same seed produces same reminder."""
    reminder1 = generate_reminder(sample_request)
    reminder2 = generate_reminder(sample_request)
    assert reminder1 == reminder2  # Same seed should produce same output


def test_generate_reminder_different_spice_levels(sample_request):
    """Test generating reminders with different spice levels."""
    reminders = []
    for spice in range(1, 6):
        req = ReminderRequest(
            message=sample_request.message,
            spice=spice,
            seed=42,
            intent=sample_request.intent,
        )
        reminder = generate_reminder(req)
        reminders.append(reminder)
    
    # All reminders should be different due to different tails
    assert len(set(reminders)) > 1


def test_generate_reminder_invalid_spice():
    """Test that invalid spice raises validation error."""
    request = ReminderRequest(message="test", spice=10)
    with pytest.raises(ValidationError):
        generate_reminder(request)


def test_generate_reminder_empty_message():
    """Test that empty message raises validation error."""
    request = ReminderRequest(message="")
    with pytest.raises(ValidationError):
        generate_reminder(request)
