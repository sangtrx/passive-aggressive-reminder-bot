from __future__ import annotations

import argparse

from .core import generate_reminder
from .data import TAILS
from .models import ReminderRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a reminder with adjustable sass.")
    parser.add_argument("message", help="What the reminder is about")
    parser.add_argument(
        "--spice",
        type=int,
        default=2,
        choices=sorted(TAILS.keys()),
        help="Sass level (1-5)",
    )
    parser.add_argument("--seed", type=int, help="Random seed for repeatability")
    return parser


def parse_args(argv: list[str] | None = None) -> ReminderRequest:
    args = build_parser().parse_args(argv)
    return ReminderRequest(message=args.message, spice=args.spice, seed=args.seed)


def main(argv: list[str] | None = None) -> None:
    request = parse_args(argv)
    print(generate_reminder(request))
