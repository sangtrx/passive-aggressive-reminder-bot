"""Configuration constants and default values."""

from enum import Enum

# Spice levels (sass levels)
MIN_SPICE = 1
MAX_SPICE = 5
DEFAULT_SPICE = 2

# Intent types
class Intent(str, Enum):
    """Reminder intent types."""
    NUDGE = "nudge"
    FOLLOW_UP = "follow_up"
    DEADLINE = "deadline"
    CHECK_IN = "check_in"

# Output channels
class Channel(str, Enum):
    """Output format channels."""
    PLAIN = "plain"
    SLACK = "slack"
    DISCORD = "discord"
    EMAIL = "email"

# Profile defaults
DEFAULT_PRONOUNS = "they/them"
DEFAULT_SIGNOFF = "Thanks"

# Schedule statuses
class ScheduleStatus(str, Enum):
    """Schedule reminder status."""
    PENDING = "pending"
    SENT = "sent"

# History limits
DEFAULT_HISTORY_LIMIT = 10
MAX_HISTORY_LIMIT = 1000

# Messages
MSG_NO_PROFILES = "No profiles saved yet."
MSG_PROFILE_SAVED = "Saved profile '{}'."
MSG_PROFILE_NOT_FOUND = "Profile '{}' not found."
MSG_PROFILE_REMOVED = "Removed profile '{}'."
MSG_NO_SCHEDULES = "No scheduled reminders found."
MSG_NO_REMINDERS_DUE = "No reminders are due."
MSG_REMINDER_SCHEDULED = "Scheduled reminder #{} for {}"
MSG_DRY_RUN_COMPLETE = "Dry run complete — no reminders were marked as sent."
MSG_NO_HISTORY = "No reminder history yet."
MSG_PROFILE_NOT_FOUND_STDERR = "Profile '{}' not found; using defaults."

# Datetime formats
DATETIME_ISO_DISPLAY = "minutes"  # Used with isoformat(timespec=...)
