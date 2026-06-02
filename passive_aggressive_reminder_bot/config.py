"""Configuration management for the reminder bot."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class BotConfig:
    """Bot configuration settings.
    
    Attributes:
        data_path: Path to data storage (JSON or SQLite)
        verbose: Enable verbose/debug logging
        auto_save: Automatically save changes to storage
        max_history: Maximum history entries to keep
    """
    data_path: Path = Path("reminder_bot_data.json")
    verbose: bool = False
    auto_save: bool = True
    max_history: int = 1000
    
    @classmethod
    def from_env(cls) -> BotConfig:
        """Load config from environment variables and defaults."""
        import os
        return cls(
            data_path=Path(os.getenv("REMINDER_DATA", "reminder_bot_data.json")),
            verbose=os.getenv("REMINDER_VERBOSE", "0").lower() in ("1", "true", "yes"),
            auto_save=os.getenv("REMINDER_AUTO_SAVE", "1").lower() in ("1", "true", "yes"),
            max_history=int(os.getenv("REMINDER_MAX_HISTORY", "1000")),
        )
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "data_path": str(self.data_path),
            "verbose": self.verbose,
            "auto_save": self.auto_save,
            "max_history": self.max_history,
        }


# Global config instance
_config: BotConfig | None = None


def get_config() -> BotConfig:
    """Get the global bot configuration."""
    global _config
    if _config is None:
        _config = BotConfig.from_env()
    return _config


def set_config(config: BotConfig) -> None:
    """Set the global bot configuration."""
    global _config
    _config = config
