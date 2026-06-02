"""Tests for channel formatting."""

import pytest
from passive_aggressive_reminder_bot.channels import format_for_channel


class TestFormatForChannel:
    """Tests for channel formatting."""
    
    def test_plain_format(self):
        """Test plain text format (no changes)."""
        reminder = "submit the report"
        result = format_for_channel("plain", reminder)
        assert result == reminder
    
    def test_slack_format(self):
        """Test Slack format with bell emoji."""
        reminder = "submit the report"
        result = format_for_channel("slack", reminder)
        assert ":bell:" in result
        assert reminder in result
    
    def test_discord_format(self):
        """Test Discord format with bell emoji."""
        reminder = "submit the report"
        result = format_for_channel("discord", reminder)
        assert "🔔" in result
        assert reminder in result
    
    def test_email_format_with_subject(self):
        """Test email format with custom subject."""
        reminder = "Please submit the report"
        subject = "Action Required"
        result = format_for_channel("email", reminder, subject=subject)
        assert f"Subject: {subject}" in result
        assert reminder in result
        assert "\n" in result
    
    def test_email_format_with_default_subject(self):
        """Test email format with default subject."""
        reminder = "Please submit the report"
        result = format_for_channel("email", reminder)
        assert "Subject: Friendly reminder" in result
        assert reminder in result
    
    def test_case_insensitive_channels(self):
        """Test that channel names are case-insensitive."""
        reminder = "test"
        assert format_for_channel("Slack", reminder) == format_for_channel("slack", reminder)
        assert format_for_channel("DISCORD", reminder) == format_for_channel("discord", reminder)
        assert format_for_channel("Email", reminder) == format_for_channel("email", reminder)
    
    def test_none_channel_defaults_to_plain(self):
        """Test that None channel defaults to plain format."""
        reminder = "test"
        result = format_for_channel(None, reminder)
        assert result == reminder
    
    def test_unknown_channel_defaults_to_plain(self):
        """Test that unknown channels default to plain format."""
        reminder = "test"
        result = format_for_channel("unknown", reminder)
        assert result == reminder
