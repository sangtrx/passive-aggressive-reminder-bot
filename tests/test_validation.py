"""Tests for input validation."""

import pytest
from datetime import datetime
from passive_aggressive_reminder_bot.validation import (
    ValidationError,
    validate_spice,
    validate_profile_name,
    validate_message,
    validate_datetime,
)


class TestValidateSpice:
    """Tests for spice validation."""
    
    def test_valid_spice_levels(self):
        """Test all valid spice levels."""
        for spice in range(1, 6):
            assert validate_spice(spice) == spice
    
    def test_invalid_spice_too_low(self):
        """Test spice level too low."""
        with pytest.raises(ValidationError):
            validate_spice(0)
    
    def test_invalid_spice_too_high(self):
        """Test spice level too high."""
        with pytest.raises(ValidationError):
            validate_spice(6)
    
    def test_invalid_spice_non_integer(self):
        """Test non-integer spice."""
        with pytest.raises(ValidationError):
            validate_spice("2")


class TestValidateProfileName:
    """Tests for profile name validation."""
    
    def test_valid_names(self):
        """Test valid profile names."""
        names = ["alex", "Alex", "alice_bob", "profile-1", "alice_bob_123"]
        for name in names:
            assert validate_profile_name(name) == name
    
    def test_empty_name(self):
        """Test empty profile name."""
        with pytest.raises(ValidationError):
            validate_profile_name("")
    
    def test_invalid_characters(self):
        """Test profile name with invalid characters."""
        invalid_names = ["alice@bob", "alice bob", "alice!", "alice.bob"]
        for name in invalid_names:
            with pytest.raises(ValidationError):
                validate_profile_name(name)
    
    def test_name_too_long(self):
        """Test profile name that's too long."""
        long_name = "a" * 51
        with pytest.raises(ValidationError):
            validate_profile_name(long_name)


class TestValidateMessage:
    """Tests for message validation."""
    
    def test_valid_messages(self):
        """Test valid messages."""
        messages = ["test", "update the roadmap", "a" * 500]
        for msg in messages:
            assert validate_message(msg) == msg
    
    def test_empty_message(self):
        """Test empty message."""
        with pytest.raises(ValidationError):
            validate_message("")
    
    def test_message_too_long(self):
        """Test message that's too long."""
        long_msg = "a" * 501
        with pytest.raises(ValidationError):
            validate_message(long_msg)
    
    def test_message_with_whitespace(self):
        """Test message with leading/trailing whitespace."""
        msg = "  test message  "
        assert validate_message(msg) == "test message"


class TestValidateDatetime:
    """Tests for datetime validation."""
    
    def test_valid_iso_datetime(self):
        """Test valid ISO format datetime."""
        dt_str = "2026-06-03T09:00:00"
        result = validate_datetime(dt_str)
        assert isinstance(result, datetime)
        assert result.year == 2026
    
    def test_invalid_datetime_format(self):
        """Test invalid datetime format."""
        with pytest.raises(ValidationError):
            validate_datetime("not-a-date")
    
    def test_invalid_datetime_values(self):
        """Test invalid datetime values."""
        with pytest.raises(ValidationError):
            validate_datetime("2026-13-01T00:00:00")
