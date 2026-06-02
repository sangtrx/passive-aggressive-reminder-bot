from __future__ import annotations


def format_for_channel(channel: str, reminder: str, subject: str | None = None) -> str:
    normalized = (channel or "plain").lower()
    if normalized == "slack":
        return f":bell: {reminder}"
    if normalized == "discord":
        return f"🔔 {reminder}"
    if normalized == "email":
        subject_line = subject or "Friendly reminder"
        return f"Subject: {subject_line}\n\n{reminder}"
    return reminder
