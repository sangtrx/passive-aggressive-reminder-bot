"""Channel-specific formatting for reminder output."""

from __future__ import annotations


def format_for_channel(channel: str, reminder: str, subject: str | None = None) -> str:
    """Format a reminder message for a specific communication channel.
    
    Applies channel-specific formatting such as emojis, headers, or markup.
    
    Args:
        channel: Target channel ('plain', 'slack', 'discord', 'email')
        reminder: The reminder message text
        subject: Optional subject line for email format
        
    Returns:
        Formatted reminder text suitable for the channel
    """
    normalized = (channel or "plain").lower()
    if normalized == "slack":
        return f":bell: {reminder}"
    if normalized == "discord":
        return f"🔔 {reminder}"
    if normalized == "email":
        subject_line = subject or "Friendly reminder"
        return f"Subject: {subject_line}\n\n{reminder}"
    return reminder
