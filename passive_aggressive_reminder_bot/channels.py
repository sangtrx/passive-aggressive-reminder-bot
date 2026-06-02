"""Channel-specific formatting for reminder output."""

from __future__ import annotations

from .constants import Channel


def format_for_channel(channel: str | Channel, reminder: str, subject: str | None = None) -> str:
    """Format a reminder message for a specific communication channel.
    
    Applies channel-specific formatting such as emojis, headers, or markup.
    
    Args:
        channel: Target channel ('plain', 'slack', 'discord', 'email')
        reminder: The reminder message text
        subject: Optional subject line for email format
        
    Returns:
        Formatted reminder text suitable for the channel
    """
    normalized = channel.value if isinstance(channel, Channel) else (channel or "plain").lower()
    if normalized == Channel.SLACK.value:
        return f":bell: {reminder}"
    if normalized == Channel.DISCORD.value:
        return f"🔔 {reminder}"
    if normalized == Channel.EMAIL.value:
        subject_line = subject or "Friendly reminder"
        return f"Subject: {subject_line}\n\n{reminder}"
    return reminder
