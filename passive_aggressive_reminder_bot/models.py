from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Profile:
    name: str
    display_name: str
    pronouns: str
    signoff: str
    default_spice: int = 2

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "Profile":
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
    message: str
    spice: int = 2
    seed: int | None = None
    intent: str = "nudge"
    profile: str | None = None
    channel: str = "plain"


@dataclass(frozen=True)
class ReminderEvent:
    timestamp: datetime
    message: str
    spice: int
    intent: str
    channel: str
    profile: str | None

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(timespec="seconds"),
            "message": self.message,
            "spice": self.spice,
            "intent": self.intent,
            "channel": self.channel,
            "profile": self.profile,
        }
