"""Storage backends for profiles, history, and schedules (JSON and SQLite)."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from .models import Profile, ReminderEvent, ScheduledReminder

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = REPO_ROOT / "reminder_bot_data.json"
DEFAULT_STORE = {"profiles": {}, "history": [], "schedules": []}


def _is_sqlite_path(path: Path) -> bool:
    return path.suffix.lower() in {".db", ".sqlite", ".sqlite3"}


def _connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def _init_db(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            name TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            pronouns TEXT NOT NULL,
            signoff TEXT NOT NULL,
            default_spice INTEGER NOT NULL
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            message TEXT NOT NULL,
            spice INTEGER NOT NULL,
            intent TEXT NOT NULL,
            channel TEXT NOT NULL,
            profile TEXT
        );
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            spice INTEGER NOT NULL,
            intent TEXT NOT NULL,
            channel TEXT NOT NULL,
            profile TEXT,
            due_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL
        );
        """
    )
    connection.commit()


def load_store(path: Path = DEFAULT_DATA_PATH) -> dict:
    if not path.exists():
        return dict(DEFAULT_STORE)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_STORE)
    if not isinstance(data, dict):
        return dict(DEFAULT_STORE)
    if not isinstance(data.get("profiles"), dict):
        data["profiles"] = {}
    if not isinstance(data.get("history"), list):
        data["history"] = []
    if not isinstance(data.get("schedules"), list):
        data["schedules"] = []
    return data


def save_store(store: dict, path: Path = DEFAULT_DATA_PATH) -> None:
    path.write_text(json.dumps(store, indent=2), encoding="utf-8")


def load_profiles(path: Path = DEFAULT_DATA_PATH) -> dict[str, Profile]:
    if _is_sqlite_path(path):
        return _load_profiles_sqlite(path)
    store = load_store(path)
    profiles: dict[str, Profile] = {}
    raw_profiles = store.get("profiles", {})
    if isinstance(raw_profiles, dict):
        for name, payload in raw_profiles.items():
            if isinstance(payload, dict):
                profiles[name] = Profile.from_dict(name, payload)
    return profiles


def upsert_profile(profile: Profile, path: Path = DEFAULT_DATA_PATH) -> None:
    if _is_sqlite_path(path):
        _upsert_profile_sqlite(profile, path)
        return
    store = load_store(path)
    profiles = store.setdefault("profiles", {})
    if isinstance(profiles, dict):
        profiles[profile.name] = profile.to_dict()
    save_store(store, path)


def delete_profile(name: str, path: Path = DEFAULT_DATA_PATH) -> bool:
    if _is_sqlite_path(path):
        return _delete_profile_sqlite(name, path)
    store = load_store(path)
    profiles = store.get("profiles", {})
    if isinstance(profiles, dict) and name in profiles:
        del profiles[name]
        save_store(store, path)
        return True
    return False


def append_history(event: ReminderEvent, path: Path = DEFAULT_DATA_PATH) -> None:
    if _is_sqlite_path(path):
        _append_history_sqlite(event, path)
        return
    store = load_store(path)
    history = store.setdefault("history", [])
    if isinstance(history, list):
        history.append(event.to_dict())
    save_store(store, path)


def list_history(path: Path = DEFAULT_DATA_PATH, limit: int = 10) -> list[ReminderEvent]:
    if _is_sqlite_path(path):
        return _list_history_sqlite(path, limit)
    store = load_store(path)
    history = store.get("history", [])
    if not isinstance(history, list):
        return []
    events = [ReminderEvent.from_dict(item) for item in history if isinstance(item, dict)]
    return list(reversed(events))[:limit]


def add_schedule(
    schedule: ScheduledReminder,
    path: Path = DEFAULT_DATA_PATH,
) -> ScheduledReminder:
    if _is_sqlite_path(path):
        return _add_schedule_sqlite(schedule, path)
    store = load_store(path)
    schedules = store.setdefault("schedules", [])
    if not isinstance(schedules, list):
        schedules = []
        store["schedules"] = schedules
    next_id = max((item.get("id", 0) for item in schedules if isinstance(item, dict)), default=0)
    saved = ScheduledReminder(
        id=next_id + 1,
        message=schedule.message,
        spice=schedule.spice,
        intent=schedule.intent,
        channel=schedule.channel,
        profile=schedule.profile,
        due_at=schedule.due_at,
        created_at=schedule.created_at,
        status=schedule.status,
    )
    schedules.append(saved.to_dict())
    save_store(store, path)
    return saved


def list_schedules(
    path: Path = DEFAULT_DATA_PATH,
    status: str | None = None,
) -> list[ScheduledReminder]:
    if _is_sqlite_path(path):
        return _list_schedules_sqlite(path, status)
    store = load_store(path)
    schedules = store.get("schedules", [])
    if not isinstance(schedules, list):
        return []
    result = [ScheduledReminder.from_dict(item) for item in schedules if isinstance(item, dict)]
    if status:
        result = [item for item in result if item.status == status]
    return sorted(result, key=lambda item: item.due_at)


def list_due_schedules(
    now: datetime,
    path: Path = DEFAULT_DATA_PATH,
) -> list[ScheduledReminder]:
    if _is_sqlite_path(path):
        return _list_due_schedules_sqlite(now, path)
    schedules = list_schedules(path, status="pending")
    return [item for item in schedules if item.due_at <= now]


def mark_schedule_sent(schedule_id: int, path: Path = DEFAULT_DATA_PATH) -> bool:
    if _is_sqlite_path(path):
        return _mark_schedule_sent_sqlite(schedule_id, path)
    store = load_store(path)
    schedules = store.get("schedules", [])
    if not isinstance(schedules, list):
        return False
    updated = False
    for item in schedules:
        if isinstance(item, dict) and item.get("id") == schedule_id:
            item["status"] = "sent"
            updated = True
    if updated:
        save_store(store, path)
    return updated


def _load_profiles_sqlite(path: Path) -> dict[str, Profile]:
    with _connect(path) as connection:
        _init_db(connection)
        rows = connection.execute("SELECT * FROM profiles").fetchall()
    profiles: dict[str, Profile] = {}
    for row in rows:
        profiles[row["name"]] = Profile(
            name=row["name"],
            display_name=row["display_name"],
            pronouns=row["pronouns"],
            signoff=row["signoff"],
            default_spice=int(row["default_spice"]),
        )
    return profiles


def _upsert_profile_sqlite(profile: Profile, path: Path) -> None:
    with _connect(path) as connection:
        _init_db(connection)
        connection.execute(
            """
            INSERT INTO profiles (name, display_name, pronouns, signoff, default_spice)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                display_name=excluded.display_name,
                pronouns=excluded.pronouns,
                signoff=excluded.signoff,
                default_spice=excluded.default_spice;
            """
            ,
            (
                profile.name,
                profile.display_name,
                profile.pronouns,
                profile.signoff,
                profile.default_spice,
            ),
        )
        connection.commit()


def _delete_profile_sqlite(name: str, path: Path) -> bool:
    with _connect(path) as connection:
        _init_db(connection)
        cursor = connection.execute("DELETE FROM profiles WHERE name = ?", (name,))
        connection.commit()
    return cursor.rowcount > 0


def _append_history_sqlite(event: ReminderEvent, path: Path) -> None:
    with _connect(path) as connection:
        _init_db(connection)
        connection.execute(
            """
            INSERT INTO history (timestamp, message, spice, intent, channel, profile)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            ,
            (
                event.timestamp.isoformat(timespec="seconds"),
                event.message,
                event.spice,
                event.intent,
                event.channel,
                event.profile,
            ),
        )
        connection.commit()


def _list_history_sqlite(path: Path, limit: int) -> list[ReminderEvent]:
    with _connect(path) as connection:
        _init_db(connection)
        rows = connection.execute(
            "SELECT * FROM history ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        ReminderEvent(
            timestamp=datetime.fromisoformat(row["timestamp"]),
            message=row["message"],
            spice=int(row["spice"]),
            intent=row["intent"],
            channel=row["channel"],
            profile=row["profile"],
        )
        for row in rows
    ]


def _add_schedule_sqlite(schedule: ScheduledReminder, path: Path) -> ScheduledReminder:
    with _connect(path) as connection:
        _init_db(connection)
        cursor = connection.execute(
            """
            INSERT INTO schedules (message, spice, intent, channel, profile, due_at, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            ,
            (
                schedule.message,
                schedule.spice,
                schedule.intent,
                schedule.channel,
                schedule.profile,
                schedule.due_at.isoformat(timespec="seconds"),
                schedule.created_at.isoformat(timespec="seconds"),
                schedule.status,
            ),
        )
        connection.commit()
        schedule_id = cursor.lastrowid
    return ScheduledReminder(
        id=int(schedule_id),
        message=schedule.message,
        spice=schedule.spice,
        intent=schedule.intent,
        channel=schedule.channel,
        profile=schedule.profile,
        due_at=schedule.due_at,
        created_at=schedule.created_at,
        status=schedule.status,
    )


def _list_schedules_sqlite(path: Path, status: str | None) -> list[ScheduledReminder]:
    with _connect(path) as connection:
        _init_db(connection)
        if status:
            rows = connection.execute(
                "SELECT * FROM schedules WHERE status = ? ORDER BY due_at",
                (status,),
            ).fetchall()
        else:
            rows = connection.execute("SELECT * FROM schedules ORDER BY due_at").fetchall()
    return [
        ScheduledReminder(
            id=int(row["id"]),
            message=row["message"],
            spice=int(row["spice"]),
            intent=row["intent"],
            channel=row["channel"],
            profile=row["profile"],
            due_at=datetime.fromisoformat(row["due_at"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            status=row["status"],
        )
        for row in rows
    ]


def _list_due_schedules_sqlite(now: datetime, path: Path) -> list[ScheduledReminder]:
    with _connect(path) as connection:
        _init_db(connection)
        rows = connection.execute(
            """
            SELECT * FROM schedules
            WHERE status = 'pending' AND due_at <= ?
            ORDER BY due_at
            """
            ,
            (now.isoformat(timespec="seconds"),),
        ).fetchall()
    return [
        ScheduledReminder(
            id=int(row["id"]),
            message=row["message"],
            spice=int(row["spice"]),
            intent=row["intent"],
            channel=row["channel"],
            profile=row["profile"],
            due_at=datetime.fromisoformat(row["due_at"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            status=row["status"],
        )
        for row in rows
    ]


def _mark_schedule_sent_sqlite(schedule_id: int, path: Path) -> bool:
    with _connect(path) as connection:
        _init_db(connection)
        cursor = connection.execute(
            "UPDATE schedules SET status = 'sent' WHERE id = ?",
            (schedule_id,),
        )
        connection.commit()
    return cursor.rowcount > 0
