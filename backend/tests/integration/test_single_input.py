from __future__ import annotations

import json
from io import StringIO

from app.cli.main import main


def test_cli_accepts_single_json_argument(monkeypatch, capsys):
    payload = json.dumps(
        {
            "message_id": "msg-1",
            "recipient": "Alice",
            "channel": "EMAIL",
            "priority": "High",
            "content": " hello ",
            "created_at": "2026-05-15T10:30:00Z",
        }
    )

    monkeypatch.setattr("sys.stdin", StringIO(""))
    code = main([payload])
    captured = capsys.readouterr()

    assert code == 0
    assert captured.err == ""
    assert json.loads(captured.out.strip()) == {
        "message_id": "msg-1",
        "recipient": "Alice",
        "channel": "email",
        "priority": "high",
        "content": "hello",
        "created_at": "2026-05-15T10:30:00Z",
    }


def test_cli_accepts_single_json_via_stdin(monkeypatch, capsys):
    payload = json.dumps(
        {
            "message_id": "msg-2",
            "recipient": "Bob",
            "channel": "sms",
            "priority": "low",
            "content": " ping ",
            "created_at": "2026-05-15T11:30:00Z",
        }
    )

    monkeypatch.setattr("sys.stdin", StringIO(payload))
    code = main([])
    captured = capsys.readouterr()

    assert code == 0
    assert captured.err == ""
    assert json.loads(captured.out.strip()) == {
        "message_id": "msg-2",
        "recipient": "Bob",
        "channel": "sms",
        "priority": "low",
        "content": "ping",
        "created_at": "2026-05-15T11:30:00Z",
    }
