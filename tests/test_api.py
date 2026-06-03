import importlib


def test_create_app_factory_exists():
    mod = importlib.import_module("passive_aggressive_reminder_bot.api")
    assert hasattr(mod, "create_app")
