"""Custom exceptions for the reminder bot."""


class ReminderBotError(Exception):
    """Base exception for all reminder bot errors."""
    pass


class ValidationError(ReminderBotError):
    """Raised when input validation fails."""
    pass


class StorageError(ReminderBotError):
    """Raised when storage operations fail."""
    pass


class ProfileNotFoundError(ReminderBotError):
    """Raised when a requested profile is not found."""
    pass


class ScheduleError(ReminderBotError):
    """Raised when schedule operations fail."""
    pass


class ConfigError(ReminderBotError):
    """Raised when configuration is invalid."""
    pass
