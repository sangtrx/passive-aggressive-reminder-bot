"""Tests for data models."""

import pytest
from datetime import datetime
from passive_aggressive_reminder_bot.models import (
    Profile,
    ReminderRequest,
    ReminderEvent,
    ScheduledReminder,
)


class TestProfile:
    """Tests for Profile model."""
    
    def test_profile_creation(self):
        """Test creating a profile."""
        profile = Profile(
            name="alex",
            display_name="Alex",
            pronouns="they/them",
            signoff="Thanks",
            default_spice=3,
        )
        assert profile.name == "alex"
        assert profile.display_name == "Alex"
        assert profile.pronouns == "they/them"
        assert profile.default_spice == 3
    
    def test_profile_frozen(self):
        """Test that profiles are immutable."""
        profile = Profile(
            name="alex",
            display_name="Alex",
            pronouns="they/them",
            signoff="Thanks",
        )
        with pytest.raises(AttributeError):
            profile.name = "bob"
    
    def test_profile_from_dict(self):
        """Test creating a profile from a dictionary."""
        data = {
            "display_name": "Alexander",
            "pronouns": "he/him",
            "signoff": "Best",
            "default_spice": 4,
        }
        profile = Profile.from_dict("alex", data)
        assert profile.name == "alex"
        assert profile.display_name == "Alexander"
        assert profile.default_spice == 4
    
    def test_profile_from_dict_with_defaults(self):
        """Test profile from dict uses defaults for missing fields."""
        data = {"display_name": "Alex"}
        profile = Profile.from_dict("alex", data)
        assert profile.pronouns == "they/them"
        assert profile.signoff == "Thanks"
        assert profile.default_spice == 2
    
    def test_profile_to_dict(self):
        """Test converting a profile to a dictionary."""
        profile = Profile(
            name="alex",
            display_name="Alex",
            pronouns="they/them",
            signoff="Thanks",
            default_spice=3,
        )
        data = profile.to_dict()
        assert data["display_name"] == "Alex"
        assert data["pronouns"] == "they/them"
        assert data["default_spice"] == 3


class TestReminderRequest:
    """Tests for ReminderRequest model."""
    
    def test_reminder_request_creation(self):
        """Test creating a reminder request."""
        request = ReminderRequest(
            message="update the docs",
            spice=3,
            seed=42,
            intent="follow_up",
            profile="alex",
            channel="slack",
        )
        assert request.message == "update the docs"
        assert request.spice == 3
        assert request.seed == 42
        assert request.intent == "follow_up"
    
    def test_reminder_request_defaults(self):
        """Test reminder request with default values."""
        request = ReminderRequest(message="test")
        assert request.spice == 2
        assert request.seed is None
        assert request.intent == "nudge"
        assert request.channel == "plain"
        assert request.profile is None


class TestReminderEvent:
    """Tests for ReminderEvent model."""
    
    def test_reminder_event_creation(self):
        """Test creating a reminder event."""
        ts = datetime(2026, 6, 1, 10, 0, 0)
        event = ReminderEvent(
            timestamp=ts,
            message="test reminder",
            spice=2,
            intent="nudge",
            channel="plain",
            profile="alex",
        )
        assert event.timestamp == ts
        assert event.message == "test reminder"
        assert event.profile == "alex"
    
    def test_reminder_event_from_dict(self):
        """Test creating a reminder event from a dictionary."""
        data = {
            "timestamp": "2026-06-01T10:00:00",
            "message": "test",
            "spice": 2,
            "intent": "nudge",
            "channel": "plain",
            "profile": "alex",
        }
        event = ReminderEvent.from_dict(data)
        assert event.message == "test"
        assert event.profile == "alex"
        assert event.timestamp.year == 2026
    
    def test_reminder_event_from_dict_with_invalid_datetime(self):
        """Test reminder event handles invalid datetime gracefully."""
        data = {
            "timestamp": "invalid-date",
            "message": "test",
            "spice": 2,
            "intent": "nudge",
            "channel": "plain",
        }
        event = ReminderEvent.from_dict(data)
        assert event.message == "test"
        # Should have set to current time or default
        assert event.timestamp is not None
    
    def test_reminder_event_to_dict(self):
        """Test converting a reminder event to a dictionary."""
        ts = datetime(2026, 6, 1, 10, 0, 0)
        event = ReminderEvent(
            timestamp=ts,
            message="test",
            spice=2,
            intent="nudge",
            channel="plain",
            profile="alex",
        )
        data = event.to_dict()
        assert data["message"] == "test"
        assert data["timestamp"] == "2026-06-01T10:00:00"
        assert data["profile"] == "alex"


class TestScheduledReminder:
    """Tests for ScheduledReminder model."""
    
    def test_scheduled_reminder_creation(self):
        """Test creating a scheduled reminder."""
        now = datetime.now()
        later = datetime(2026, 6, 10, 9, 0, 0)
        reminder = ScheduledReminder(
            id=1,
            message="send report",
            spice=2,
            intent="deadline",
            channel="email",
            profile="alex",
            due_at=later,
            created_at=now,
            status="pending",
        )
        assert reminder.id == 1
        assert reminder.message == "send report"
        assert reminder.status == "pending"
    
    def test_scheduled_reminder_default_status(self):
        """Test scheduled reminder defaults to pending status."""
        now = datetime.now()
        reminder = ScheduledReminder(
            id=1,
            message="test",
            spice=2,
            intent="nudge",
            channel="plain",
            profile=None,
            due_at=now,
            created_at=now,
        )
        assert reminder.status == "pending"
