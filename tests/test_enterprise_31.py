import pytest
from passive_aggressive_reminder_bot import generate_reminder


def test_generate_reminder_smoke_31():
    req = {
        'message': 'do task 31',
        'spice': 2,
        'intent': 'nudge',
        'channel': 'plain'
    }
    r = generate_reminder(type('R', (), req)(), None) if hasattr(generate_reminder, '__call__') else True
    assert r is not None

