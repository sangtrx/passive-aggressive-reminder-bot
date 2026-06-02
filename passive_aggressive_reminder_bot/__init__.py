"""Passive-Aggressive Reminder Bot — Generate sassy reminders with style.

This package provides a CLI and Python API for generating reminders with
configurable sass levels and personality. Use it to schedule passive-aggressive
reminders via JSON or SQLite storage.

Core API:
    - generate_reminder() — Generate a single reminder message
    - Profile — User profile with personalization settings
    - ReminderRequest — Parameters for generating a reminder
    - ScheduledReminder — Stored scheduled reminder

Example:
    >>> from passive_aggressive_reminder_bot import generate_reminder, Profile, ReminderRequest
    >>> profile = Profile("alice", "Alice", "they/them", "Thanks", 2)
    >>> request = ReminderRequest("submit the report", spice=4, profile="alice")
    >>> reminder = generate_reminder(request, profile)
"""

__version__ = "0.2.0"

from .core import generate_reminder
from .models import Profile, ReminderEvent, ReminderRequest, ScheduledReminder

__all__ = [
    "Profile",
    "ReminderRequest",
    "ReminderEvent",
    "ScheduledReminder",
    "generate_reminder",
    "__version__",
]
