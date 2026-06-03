"""Command-line interface for the passive-aggressive reminder bot."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .channels import format_for_channel
from .constants import (
    CHANNELS,
    INTENT_TEMPLATES,
    MSG_DRY_RUN_COMPLETE,
    MSG_NO_HISTORY,
    MSG_NO_PROFILES,
    MSG_NO_REMINDERS_DUE,
    MSG_NO_SCHEDULES,
    MSG_PROFILE_NOT_FOUND,
    MSG_PROFILE_NOT_FOUND_STDERR,
    MSG_PROFILE_REMOVED,
    MSG_PROFILE_SAVED,
    MSG_REMINDER_SCHEDULED,
    TAILS,
)
from . import __version__
from .core import generate_reminder
from .models import Profile, ReminderEvent, ReminderRequest, ScheduledReminder
from .storage import (
    DEFAULT_DATA_PATH,
    add_schedule,
    append_history,
    delete_profile,
    list_due_schedules,
    list_history,
    list_schedules,
    load_profiles,
    mark_schedule_sent,
    upsert_profile,
)


def parse_datetime(value: str) -> datetime:
    """Parse an ISO format datetime string."""
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Datetime must be ISO format (e.g. 2026-06-03T09:00)"
        ) from exc


def _add_data_argument(parser: argparse.ArgumentParser) -> None:
    """Add the shared data-store argument to a parser."""
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )


def build_parser() -> tuple[argparse.ArgumentParser, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description="Generate a reminder with adjustable sass.")
    parser.add_argument("--version", action="version", version=f"passive-aggressive-reminder-bot {__version__}")
    parser.add_argument("--enterprise-key", help="Enterprise API key for admin operations", default=None)
    subparsers = parser.add_subparsers(dest="command")

    export_parser = subparsers.add_parser("export", help="Export schedules to a JSON file")
    export_parser.add_argument("--output", "-o", help="Output JSON file", default="schedules_export.json")
    _add_data_argument(export_parser)

    remind_parser = subparsers.add_parser("remind", help="Generate a reminder")
    remind_parser.add_argument("message", help="What the reminder is about")
    remind_parser.add_argument(
        "--spice",
        type=int,
        default=None,
        choices=sorted(TAILS.keys()),
        help="Sass level (1-5)",
    )
    remind_parser.add_argument("--seed", type=int, help="Random seed for repeatability")
    remind_parser.add_argument(
        "--intent",
        choices=sorted(INTENT_TEMPLATES.keys()),
        default="nudge",
        help="Message intent",
    )
    remind_parser.add_argument("--profile", help="Profile name to personalize")
    remind_parser.add_argument(
        "--channel",
        choices=CHANNELS,
        default="plain",
        help="Output channel formatting",
    )
    _add_data_argument(remind_parser)

    profile_parser = subparsers.add_parser("profile", help="Manage profiles")
    profile_sub = profile_parser.add_subparsers(dest="profile_command", required=True)

    profile_add = profile_sub.add_parser("add", help="Add or update a profile")
    profile_add.add_argument("name", help="Profile key (used for lookups)")
    profile_add.add_argument("--display-name", dest="display_name", help="Name to greet")
    profile_add.add_argument("--pronouns", default="they/them")
    profile_add.add_argument("--signoff", default="Thanks")
    profile_add.add_argument(
        "--default-spice",
        type=int,
        default=2,
        choices=sorted(TAILS.keys()),
    )
    _add_data_argument(profile_add)

    profile_list = profile_sub.add_parser("list", help="List saved profiles")
    _add_data_argument(profile_list)

    profile_remove = profile_sub.add_parser("remove", help="Remove a profile")
    profile_remove.add_argument("name", help="Profile key to remove")
    _add_data_argument(profile_remove)

    schedule_parser = subparsers.add_parser("schedule", help="Schedule reminders")
    schedule_sub = schedule_parser.add_subparsers(dest="schedule_command", required=True)

    schedule_add = schedule_sub.add_parser("add", help="Add a scheduled reminder")
    schedule_add.add_argument("message", help="What the reminder is about")
    schedule_add.add_argument("--due", type=parse_datetime, required=True)
    schedule_add.add_argument(
        "--spice",
        type=int,
        default=None,
        choices=sorted(TAILS.keys()),
    )
    schedule_add.add_argument(
        "--intent",
        choices=sorted(INTENT_TEMPLATES.keys()),
        default="nudge",
    )
    schedule_add.add_argument("--profile", help="Profile name to personalize")
    schedule_add.add_argument(
        "--channel",
        choices=CHANNELS,
        default="plain",
    )
    _add_data_argument(schedule_add)

    schedule_list = schedule_sub.add_parser("list", help="List scheduled reminders")
    schedule_list.add_argument(
        "--status",
        choices=("pending", "sent", "all"),
        default="all",
    )
    _add_data_argument(schedule_list)

    schedule_due = schedule_sub.add_parser("due", help="List due reminders")
    schedule_due.add_argument("--now", type=parse_datetime)
    _add_data_argument(schedule_due)

    schedule_send = schedule_sub.add_parser("send", help="Send due reminders")
    schedule_send.add_argument("--now", type=parse_datetime)
    schedule_send.add_argument("--dry-run", action="store_true")
    _add_data_argument(schedule_send)

    history_parser = subparsers.add_parser("history", help="Show reminder history")
    history_parser.add_argument("--limit", type=int, default=10)
    _add_data_argument(history_parser)

    return parser, remind_parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser, remind_parser = build_parser()
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    if raw_argv and raw_argv[0] not in {"remind", "profile", "schedule", "history"}:
        args = remind_parser.parse_args(raw_argv)
        args.command = "remind"
        return args
    args = parser.parse_args(raw_argv)
    if args.command is None:
        parser.print_help()
        raise SystemExit(2)
    return args


def handle_profile_commands(args: argparse.Namespace) -> None:
    data_path = args.data
    if args.profile_command == "list":
        profiles = load_profiles(data_path)
        if not profiles:
            print(MSG_NO_PROFILES)
            return
        for name, profile in sorted(profiles.items()):
            print(
                f"{name}: {profile.display_name} ({profile.pronouns}), "
                f"default spice {profile.default_spice}"
            )
        return

    if args.profile_command == "add":
        display_name = args.display_name or args.name.replace("_", " ").title()
        profile = Profile(
            name=args.name,
            display_name=display_name,
            pronouns=args.pronouns,
            signoff=args.signoff,
            default_spice=args.default_spice,
        )
        upsert_profile(profile, data_path)
        print(MSG_PROFILE_SAVED.format(profile.name))
        return

    if args.profile_command == "remove":
        removed = delete_profile(args.name, data_path)
        if removed:
            print(MSG_PROFILE_REMOVED.format(args.name))
        else:
            print(MSG_PROFILE_NOT_FOUND.format(args.name))


def handle_schedule_commands(args: argparse.Namespace) -> None:
    data_path = args.data
    profiles = load_profiles(data_path)

    if args.schedule_command == "add":
        profile = profiles.get(args.profile) if args.profile else None
        spice = args.spice if args.spice is not None else (profile.default_spice if profile else 2)
        schedule = ScheduledReminder(
            id=0,
            message=args.message,
            spice=spice,
            intent=args.intent,
            channel=args.channel,
            profile=profile.name if profile else None,
            due_at=args.due,
            created_at=datetime.now(),
            status="pending",
        )
        saved = add_schedule(schedule, data_path)
        print(MSG_REMINDER_SCHEDULED.format(saved.id, saved.due_at.isoformat(timespec="minutes")))
        return

    if args.schedule_command == "list":
        status = None if args.status == "all" else args.status
        schedules = list_schedules(data_path, status=status)
        if not schedules:
            print(MSG_NO_SCHEDULES)
            return
        for schedule in schedules:
            profile_label = f" ({schedule.profile})" if schedule.profile else ""
            print(
                f"#{schedule.id} | {schedule.due_at.isoformat(timespec='minutes')} "
                f"[{schedule.status}] {schedule.message}{profile_label}"
            )
        return

    if args.schedule_command == "due":
        now = args.now or datetime.now()
        schedules = list_due_schedules(now, data_path)
        if not schedules:
            print(MSG_NO_REMINDERS_DUE)
            return
        for schedule in schedules:
            profile_label = f" ({schedule.profile})" if schedule.profile else ""
            print(
                f"#{schedule.id} | {schedule.due_at.isoformat(timespec='minutes')} "
                f"{schedule.message}{profile_label}"
            )
        return

    if args.schedule_command == "send":
        now = args.now or datetime.now()
        schedules = list_due_schedules(now, data_path)
        if not schedules:
            print(MSG_NO_REMINDERS_DUE)
            return
        for schedule in schedules:
            profile = profiles.get(schedule.profile) if schedule.profile else None
            request = ReminderRequest(
                message=schedule.message,
                spice=schedule.spice,
                seed=None,
                intent=schedule.intent,
                profile=profile.name if profile else None,
                channel=schedule.channel,
            )
            reminder = generate_reminder(request, profile)
            subject = f"Reminder: {schedule.message}"
            output = format_for_channel(schedule.channel, reminder, subject=subject)
            print(f"\nScheduled reminder #{schedule.id}:")
            print(output)
            if not args.dry_run:
                mark_schedule_sent(schedule.id, data_path)
                append_history(
                    ReminderEvent(
                        timestamp=now,
                        message=schedule.message,
                        spice=schedule.spice,
                        intent=schedule.intent,
                        channel=schedule.channel,
                        profile=profile.name if profile else None,
                    ),
                    data_path,
                )
        if args.dry_run:
            print(f"\n{MSG_DRY_RUN_COMPLETE}")


def handle_export(args: argparse.Namespace) -> None:
    data_path = args.data
    from .storage import list_schedules
    import json

    schedules = list_schedules(data_path)
    output = args.output
    with open(output, "w", encoding="utf-8") as fh:
        json.dump([s.to_dict() for s in schedules], fh, indent=2, ensure_ascii=False)
    print(f"Exported {len(schedules)} schedules to {output}")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if args.command == "profile":
        handle_profile_commands(args)
        return

    if args.command == "schedule":
        handle_schedule_commands(args)
        return

    if args.command == "history":
        events = list_history(args.data, limit=args.limit)
        if not events:
            print(MSG_NO_HISTORY)
            return
        for event in events:
            profile_label = f" ({event.profile})" if event.profile else ""
            print(
                f"{event.timestamp.isoformat(timespec='minutes')} | "
                f"{event.intent} | {event.message}{profile_label}"
            )
        return

    data_path = args.data
    profiles = load_profiles(data_path)
    profile = profiles.get(args.profile) if args.profile else None
    if args.profile and not profile:
        print(MSG_PROFILE_NOT_FOUND_STDERR.format(args.profile), file=sys.stderr)

    spice = args.spice if args.spice is not None else (profile.default_spice if profile else 2)
    request = ReminderRequest(
        message=args.message,
        spice=spice,
        seed=args.seed,
        intent=args.intent,
        profile=profile.name if profile else None,
        channel=args.channel,
    )
    reminder = generate_reminder(request, profile)
    subject = f"Reminder: {args.message}"
    output = format_for_channel(args.channel, reminder, subject=subject)
    print(output)
    append_history(
        ReminderEvent(
            timestamp=datetime.now(),
            message=args.message,
            spice=spice,
            intent=args.intent,
            channel=args.channel,
            profile=profile.name if profile else None,
        ),
        data_path,
    )
