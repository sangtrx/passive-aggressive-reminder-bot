# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-02

### Added
- Comprehensive logging system with configurable debug output
- Input validation module with detailed error messages
- Configuration management module with environment variable support
- Custom exceptions module for better error handling
- Package entry point (`__main__.py`) for `python -m passive_aggressive_reminder_bot`
- Comprehensive test suite with 34+ tests covering:
  - Core reminder generation
  - Input validation (spice, profile names, messages, datetimes)
  - Data model serialization/deserialization
  - Profile management
- `py.typed` marker for PEP 561 type checking support
- Contributing guidelines document
- Editor configuration (`.editorconfig`) for consistent formatting
- Development dependencies file (`requirements-dev.txt`)
- Enhanced README with detailed examples and architecture documentation

### Changed
- Improved type hints throughout the codebase
- Moved validation error class to custom exceptions module
- Enhanced module docstrings with better documentation
- Updated data module with type annotations

### Security
- Added input validation for profile names, messages, and datetime strings
- Added spice level bounds checking

## [0.1.0] - 2026-05-XX

### Added
- Initial release
- Core reminder generation with 5 sass levels
- Profile management (create, list, remove)
- Scheduled reminders with JSON/SQLite storage
- Multiple output formats (plain, Slack, Discord, email)
- Command-line interface with argparse
- Support for different reminder intents (nudge, follow_up, deadline, check_in)
- Flexible data storage backend (JSON or SQLite)
