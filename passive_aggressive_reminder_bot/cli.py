from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .channels import format_for_channel
from .core import generate_reminder
from .data import CHANNELS, INTENT_TEMPLATES, TAILS
from .models import Profile, ReminderEvent, ReminderRequest
from .storage import DEFAULT_DATA_PATH, append_history, delete_profile, load_profiles, upsert_profile


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

    return parser, remind_parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser, remind_parser = build_parser()
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    if raw_argv and raw_argv[0] not in {"remind", "profile"}:
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


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if args.command == "profile":
        handle_profile_commands(args)
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
