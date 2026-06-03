import json
from pathlib import Path


def test_export_writes_file(tmp_path):
    out = tmp_path / "out.json"
    # import the cli handler and call it with a fresh store
    from passive_aggressive_reminder_bot.cli import handle_export

    class Args:
        data = tmp_path / "store.json"
        output = str(out)

    # Ensure export runs even with empty store
    handle_export(Args)
    assert out.exists()
    content = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(content, list)
