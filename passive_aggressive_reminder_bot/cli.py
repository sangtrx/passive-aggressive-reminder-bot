"""Command-line interface for the passive-aggressive reminder bot."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .channels import format_for_channel
from .core import generate_reminder
from .data import CHANNELS, INTENT_TEMPLATES, TAILS
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
        raise argparse.ArgumentTypeError("Datetime must be ISO format") from exc


def build_parser() -> tuple[argparse.ArgumentParser, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description="Generate a reminder with adjustable sass.")
    subparsers = parser.add_subparsers(dest="command")

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
    remind_parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

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
    profile_add.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

    profile_list = profile_sub.add_parser("list", help="List saved profiles")
    profile_list.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

    profile_remove = profile_sub.add_parser("remove", help="Remove a profile")
    profile_remove.add_argument("name", help="Profile key to remove")
    profile_remove.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

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
    schedule_add.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

    schedule_list = schedule_sub.add_parser("list", help="List scheduled reminders")
    schedule_list.add_argument(
        "--status",
        choices=("pending", "sent", "all"),
        default="all",
    )
    schedule_list.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

    schedule_due = schedule_sub.add_parser("due", help="List due reminders")
    schedule_due.add_argument("--now", type=parse_datetime)
    schedule_due.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

    schedule_send = schedule_sub.add_parser("send", help="Send due reminders")
    schedule_send.add_argument("--now", type=parse_datetime)
    schedule_send.add_argument("--dry-run", action="store_true")
    schedule_send.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

    history_parser = subparsers.add_parser("history", help="Show reminder history")
    history_parser.add_argument("--limit", type=int, default=10)
    history_parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to reminder data store",
    )

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
            print("No profiles saved yet.")
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
        print(f"Saved profile '{profile.name}'.")
        return

    if args.profile_command == "remove":
        removed = delete_profile(args.name, data_path)
        if removed:
            print(f"Removed profile '{args.name}'.")
        else:
            print(f"Profile '{args.name}' not found.")


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
        print(
            f"Scheduled reminder #{saved.id} for "
            f"{saved.due_at.isoformat(timespec='minutes')}"
        )
        return

    if args.schedule_command == "list":
        status = None if args.status == "all" else args.status
        schedules = list_schedules(data_path, status=status)
        if not schedules:
            print("No scheduled reminders found.")
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
            print("No reminders are due.")
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
            print("No reminders are due.")
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
            print("\nDry run complete — no reminders were marked as sent.")


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
            print("No reminder history yet.")
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
        print(f"Profile '{args.profile}' not found; using defaults.", file=sys.stderr)

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
