from __future__ import annotations

import json
from pathlib import Path

from .models import Profile, ReminderEvent

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = REPO_ROOT / "reminder_bot_data.json"
DEFAULT_STORE = {"profiles": {}, "history": []}


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
    return data


def save_store(store: dict, path: Path = DEFAULT_DATA_PATH) -> None:
    path.write_text(json.dumps(store, indent=2), encoding="utf-8")


def load_profiles(path: Path = DEFAULT_DATA_PATH) -> dict[str, Profile]:
    store = load_store(path)
    profiles: dict[str, Profile] = {}
    raw_profiles = store.get("profiles", {})
    if isinstance(raw_profiles, dict):
        for name, payload in raw_profiles.items():
            if isinstance(payload, dict):
                profiles[name] = Profile.from_dict(name, payload)
    return profiles


def upsert_profile(profile: Profile, path: Path = DEFAULT_DATA_PATH) -> None:
    store = load_store(path)
    profiles = store.setdefault("profiles", {})
    if isinstance(profiles, dict):
        profiles[profile.name] = profile.to_dict()
    save_store(store, path)


def delete_profile(name: str, path: Path = DEFAULT_DATA_PATH) -> bool:
    store = load_store(path)
    profiles = store.get("profiles", {})
    if isinstance(profiles, dict) and name in profiles:
        del profiles[name]
        save_store(store, path)
        return True
    return False


def append_history(event: ReminderEvent, path: Path = DEFAULT_DATA_PATH) -> None:
    store = load_store(path)
    history = store.setdefault("history", [])
    if isinstance(history, list):
        history.append(event.to_dict())
    save_store(store, path)
