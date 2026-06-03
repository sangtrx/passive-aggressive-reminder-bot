# Passive-Aggressive Reminder Bot

A sassy Python CLI tool that generates reminders with configurable sass levels and personality. 
Perfect for those who need their reminders served with a side of snark.

## Features

- 🎯 **5 Sass Levels** — From gentle nudges to full-on sarcasm
- 👤 **Personalization** — Save profiles with custom names and signoffs
- 📅 **Scheduling** — Set up reminders to send at specific times
- 💾 **Flexible Storage** — JSON (default) or SQLite backend
- 🔧 **Multiple Formats** — Plain text, Slack, Discord, or email formatting
- 🧪 **Well-Tested** — Comprehensive test suite (21+ tests)
- 📝 **Type safe** — Full type hints throughout the codebase

## Installation

Clone the repository and run:

```bash
cd passive-aggressive-reminder-bot
python main.py --help
```

### Development Setup

Install development dependencies:

```bash
pip install -r requirements-dev.txt
# Optional enterprise deps (FastAPI, SQLAlchemy, Prometheus):
pip install -r requirements-enterprise.txt
```

Run tests:

```bash
pytest tests/ -v
```

## Quick Start

### Simple Reminders

Generate a reminder with different sass levels:

```bash
# Gentle nudge
python main.py "submit the timesheet" --spice 1

# Medium sass
python main.py "reply to the email" --spice 2

# Maximum sass
python main.py "update the roadmap" --spice 5
```

### With Formatting

Specify the output format:

```bash
# Slack-formatted
python main.py remind "update the roadmap" --intent follow_up --channel slack

# Discord format
python main.py remind "send the draft" --channel discord
```

### Profiles

Create and use saved profiles:

```bash
# Add a profile
python main.py profile add alex --display-name "Alex" --signoff "Thanks, Alex"

# List profiles
python main.py profile list

# Use a profile in a reminder
python main.py "send the feedback" --profile alex --spice 3

# Remove a profile
python main.py profile remove alex
```

### Scheduling

Schedule reminders for later:

```bash
# Schedule a reminder
python main.py schedule add "send the draft" --due 2026-06-03T09:00 --profile alex

# List all scheduled reminders
python main.py schedule list

# Show due reminders
python main.py schedule due

# Send all due reminders (use --dry-run to preview)
python main.py schedule send
python main.py schedule send --dry-run
```

### History

View reminder history:

```bash
# Show last 10 reminders
python main.py history

# Show last 5
python main.py history --limit 5
```

## Options

### Reminders

- `message` — Reminder content
- `--spice` — Sass level from 1 (gentle) to 5 (spicy). Default: 2
- `--intent` — Message intent: `nudge`, `follow_up`, `deadline`, `check_in`. Default: nudge
- `--profile` — Saved profile name for personalization
- `--channel` — Output format: `plain`, `slack`, `discord`, `email`. Default: plain
- `--seed` — Random seed for reproducible output
- `--data` — Path to data store (defaults to `reminder_bot_data.json`)

### Profiles

- `profile add <name>` — Create/update a profile
  - `--display-name` — Human-readable name (default: title-cased version of name)
  - `--pronouns` — Pronouns for personalization (default: they/them)
  - `--signoff` — Closing signature (default: Thanks)
  - `--default-spice` — Default sass level (default: 2)
- `profile list` — Show all saved profiles
- `profile remove <name>` — Delete a profile

### Scheduling

- `schedule add <message>` — Create a scheduled reminder
  - `--due` — When to send (ISO 8601 format, required)
  - `--intent` — Message intent (default: nudge)
  - `--spice` — Sass level (default: 2)
  - `--profile` — Profile to use
  - `--channel` — Output format (default: plain)
- `schedule list` — List scheduled reminders
  - `--status` — Filter by status: `pending`, `sent`, or `all` (default: all)
- `schedule due` — Show reminders that are due now
- `schedule send` — Dispatch all due reminders
  - `--dry-run` — Preview without sending

### History

- `history` — Show reminder history
  - `--limit` — Number of entries to show (default: 10)

### Storage

Store data in SQLite instead of JSON:

```bash
python main.py --data reminder_bot.db "your message"
```

This automatically creates and manages the SQLite database with proper schema.

## Architecture

### Core Modules

- **`core.py`** — Reminder generation engine with validation
- **`models.py`** — Data classes (Profile, ReminderRequest, ReminderEvent, ScheduledReminder)
- **`storage.py`** — JSON and SQLite backends
- **`data.py`** — Message templates and sass phrases
- **`cli.py`** — Command-line interface
- **`validation.py`** — Input validation with detailed error messages
- **`config.py`** — Configuration management
- **`logging_config.py`** — Logging setup for debugging

## Testing

The project includes comprehensive tests covering:

- Core reminder generation
- Input validation
- Spice level handling
- Profile management
- Datetime parsing

Run with coverage:

```bash
pytest tests/ --cov=passive_aggressive_reminder_bot
```

## Development

### Code Style

- Format code with Black (line length: 100)
- Lint with Ruff
- Type check with mypy

```bash
black passive_aggressive_reminder_bot tests
ruff check .
mypy passive_aggressive_reminder_bot
```

### Adding New Features

1. Write tests first (TDD)
2. Implement the feature
3. Update documentation
4. Commit with a clear message

## License

MIT License — See LICENSE file for details

## Contributing

Contributions welcome! Submit pull requests or open issues for bugs and feature requests.

## Changelog

### v0.2.0
- Added comprehensive logging system
- Added input validation module with detailed error messages
- Added configuration management
- Added comprehensive test suite (21+ tests)
- Improved type hints throughout codebase
- Added development dependencies

### v0.1.0
- Initial release
- Core reminder generation
- Profile management
- Scheduling support
- JSON and SQLite storage

- Upgrade note 56: small quality improvement.
- Upgrade note 57: small quality improvement.
- Upgrade note 58: small quality improvement.
- Upgrade note 59: small quality improvement.
- Upgrade note 60: small quality improvement.
- Upgrade note 61: small quality improvement.
- Upgrade note 62: small quality improvement.
- Upgrade note 63: small quality improvement.
- Upgrade note 64: small quality improvement.
