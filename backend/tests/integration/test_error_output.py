from __future__ import annotations

import json
from io import StringIO

from app.cli.main import main


def test_cli_rejects_invalid_input(monkeypatch, capsys):
    payload = json.dumps(
        {
            "message_id": "msg-1",
            "recipient": "Alice",
            "channel": "fax",
            "priority": "high",
            "content": "hello",
            "created_at": "2026-05-15T10:30:00Z",
        }
    )

    monkeypatch.setattr("sys.stdin", StringIO(""))
    code = main([payload])
    captured = capsys.readouterr()

    assert code == 1
    assert captured.out == ""
    assert "channel" in captured.err
