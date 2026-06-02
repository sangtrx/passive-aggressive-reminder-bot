"""Data models for reminder bot profiles, requests, events, and schedules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Profile:
    """Represents a user profile with personalization settings.
    
    Attributes:
        name: Internal profile identifier (key)
        display_name: Human-readable name for personalized greetings
        pronouns: Pronouns for the profile owner (default: they/them)
        signoff: Closing signature for reminders (default: Thanks)
        default_spice: Default sass level for this profile (1-5, default: 2)
    """
    name: str
    display_name: str
    pronouns: str
    signoff: str
    default_spice: int = 2

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "Profile":
        """Create a Profile from a dictionary (deserialization)."""
        display = data.get("display_name") or name.replace("_", " ").title()
        return cls(
            name=name,
            display_name=str(display),
            pronouns=str(data.get("pronouns", "they/them")),
            signoff=str(data.get("signoff", "Thanks")),
            default_spice=int(data.get("default_spice", 2)),
        )

    def to_dict(self) -> dict:
        return {
            "display_name": self.display_name,
            "pronouns": self.pronouns,
            "signoff": self.signoff,
            "default_spice": self.default_spice,
        }


@dataclass(frozen=True)
class ReminderRequest:
    """Encapsulates parameters for generating a reminder.
    
    Attributes:
        message: The reminder message content
        spice: Sass level from 1 (gentle) to 5 (spicy)
        seed: Optional random seed for reproducible output
        intent: Type of reminder: nudge, follow_up, deadline, check_in
        profile: Optional profile name for personalization
        channel: Output format: plain, slack, discord, email
    """
    message: str
    spice: int = 2
    seed: int | None = None
    intent: str = "nudge"
    profile: str | None = None
    channel: str = "plain"


@dataclass(frozen=True)
class ReminderEvent:
    """Represents a reminder that was sent (history record).
    
    Attributes:
        timestamp: When the reminder was generated
        message: The reminder message content
        spice: Sass level that was used
        intent: Type of reminder that was sent
        channel: Output format that was used
        profile: Profile name if personalized, None otherwise
    """
    timestamp: datetime
    message: str
    spice: int
    intent: str
    channel: str
    profile: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "ReminderEvent":
        """Create a ReminderEvent from a dictionary (deserialization)."""
        raw_ts = data.get("timestamp")
        try:
            timestamp = datetime.fromisoformat(raw_ts) if raw_ts else datetime.now()
        except ValueError:
            timestamp = datetime.now()
        return cls(
            timestamp=timestamp,
            message=str(data.get("message", "")),
            spice=int(data.get("spice", 2)),
            intent=str(data.get("intent", "nudge")),
            channel=str(data.get("channel", "plain")),
            profile=data.get("profile"),
        )

    def to_dict(self) -> dict:
        """Convert ReminderEvent to a dictionary for serialization."""
        """Convert ReminderEvent to a dictionary for serialization."""
        return {
            "timestamp": self.timestamp.isoformat(timespec="seconds"),
            "message": self.message,
            "spice": self.spice,
            "intent": self.intent,
            "channel": self.channel,
            "profile": self.profile,
        }


@dataclass(frozen=True)
class ScheduledReminder:
    """Represents a reminder scheduled for future delivery.
    
    Attributes:
        id: Unique identifier for the scheduled reminder
        message: The reminder message content
        spice: Sass level for the reminder
        intent: Type of reminder
        channel: Output format for delivery
        profile: Profile name if personalized, None otherwise
        due_at: When the reminder should be sent
        created_at: When the reminder was scheduled
        status: Current state (pending, sent)
    """
    id: int
    message: str
    spice: int
    intent: str
    channel: str
    profile: str | None
    due_at: datetime
    created_at: datetime
    status: str = "pending"

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduledReminder":
        """Create a ScheduledReminder from a dictionary (deserialization)."""
        def parse_dt(value: str | None) -> datetime:
            try:
                return datetime.fromisoformat(value) if value else datetime.now()
            except ValueError:
                return datetime.now()

        return cls(
            id=int(data.get("id", 0)),
            message=str(data.get("message", "")),
            spice=int(data.get("spice", 2)),
            intent=str(data.get("intent", "nudge")),
            channel=str(data.get("channel", "plain")),
            profile=data.get("profile"),
            due_at=parse_dt(data.get("due_at")),
            created_at=parse_dt(data.get("created_at")),
            status=str(data.get("status", "pending")),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "message": self.message,
            "spice": self.spice,
            "intent": self.intent,
            "channel": self.channel,
            "profile": self.profile,
            "due_at": self.due_at.isoformat(timespec="seconds"),
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "status": self.status,
        }
