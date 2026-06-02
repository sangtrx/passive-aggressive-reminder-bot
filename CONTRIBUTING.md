# Contributing to Passive-Aggressive Reminder Bot

Thank you for your interest in contributing! This document outlines the process for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/passive-aggressive-reminder-bot.git
cd passive-aggressive-reminder-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Code Style

We follow PEP 8 with the following tools:

- **Black** — Code formatting (line length: 100)
- **Ruff** — Linting
- **mypy** — Type checking

Before submitting a PR, run:

```bash
black passive_aggressive_reminder_bot tests
ruff check . --fix
mypy passive_aggressive_reminder_bot
```

## Testing

We use pytest for testing. Ensure all tests pass before submitting:

```bash
pytest tests/ -v
```

For coverage reports:

```bash
pytest tests/ --cov=passive_aggressive_reminder_bot
```

## Commit Messages

Use clear, descriptive commit messages:

- ✅ Good: `Add validation for profile names`
- ✅ Good: `Fix scheduling timezone handling`
- ❌ Avoid: `Fix bug` or `Update code`

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Update documentation if needed
6. Run the full test suite: `pytest tests/ -v`
7. Commit with clear messages
8. Push to your fork and open a PR

## Types of Contributions

### Bug Fixes
- Create a test that reproduces the bug
- Fix the issue
- Verify the test passes

### New Features
- Discuss in an issue first (for larger features)
- Write tests using TDD (Test-Driven Development)
- Update README with new feature documentation
- Add docstrings to new functions/classes

### Documentation
- Fix typos and improve clarity
- Add examples
- Improve technical accuracy

## Code Guidelines

### Type Hints
All functions and methods should have type hints:

```python
def generate_reminder(request: ReminderRequest, profile: Profile | None = None) -> str:
    """Generate a reminder message."""
    ...
```

### Docstrings
Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> str:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
```

### Error Handling
Use custom exceptions defined in `exceptions.py`:

```python
from passive_aggressive_reminder_bot.exceptions import ValidationError

def validate(data: str) -> str:
    if not data:
        raise ValidationError("Data cannot be empty")
    return data
```

## Questions?

- Open an issue for bug reports and feature requests
- Discuss in existing issues before starting major work
- Tag issues with appropriate labels

Thank you for contributing! 🎉
