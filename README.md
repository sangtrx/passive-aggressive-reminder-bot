# Passive-Aggressive Reminder Bot

Generate reminders with a configurable spice level.

## Quick start

- `python main.py "submit the timesheet" --spice 4`
- `python main.py "reply to the email" --spice 1`
- `python main.py remind "update the roadmap" --intent follow_up --channel slack`
- `python main.py profile add alex --display-name "Alex" --signoff "Thanks, Alex"`
- `python main.py profile list`

## Options

### Reminders

- `message` — Reminder content
- `--spice` — Sass level from 1 (gentle) to 5 (spicy)
- `--intent` — `nudge`, `follow_up`, `deadline`, or `check_in`
- `--profile` — Saved profile name for personalization
- `--channel` — `plain`, `slack`, `discord`, or `email`
- `--seed` — Make the output repeatable
- `--data` — Path to the JSON data store (defaults to `reminder_bot_data.json`)

### Profiles

- `profile add <name>` — Create/update a profile
- `profile list` — Show saved profiles
- `profile remove <name>` — Delete a profile
