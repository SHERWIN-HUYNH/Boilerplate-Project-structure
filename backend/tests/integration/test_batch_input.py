from __future__ import annotations

import json
from io import StringIO

from app.cli.main import main


def test_cli_accepts_jsonl_batch_from_file(monkeypatch, capsys, tmp_path):
    batch = tmp_path / "input.jsonl"
    batch.write_text(
        "\n".join(
            [
                json.dumps({"message_id": "msg-1", "recipient": "Alice", "channel": "email", "priority": "high", "content": "hello", "created_at": "2026-05-15T10:30:00Z"}),
                json.dumps({"message_id": "msg-2", "recipient": "Bob", "channel": "sms", "priority": "low", "content": "ping", "created_at": "2026-05-15T11:30:00Z"}),
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.stdin", StringIO(""))
    code = main([str(batch)])
    captured = capsys.readouterr()

    assert code == 0
    assert captured.err == ""
    lines = [json.loads(line) for line in captured.out.strip().splitlines()]
    assert lines == [
        {"message_id": "msg-1", "recipient": "Alice", "channel": "email", "priority": "high", "content": "hello", "created_at": "2026-05-15T10:30:00Z"},
        {"message_id": "msg-2", "recipient": "Bob", "channel": "sms", "priority": "low", "content": "ping", "created_at": "2026-05-15T11:30:00Z"},
    ]


def test_cli_accepts_jsonl_batch_via_stdin(monkeypatch, capsys):
    batch = "\n".join(
        [
            json.dumps({"message_id": "msg-1", "recipient": "Alice", "channel": "email", "priority": "high", "content": "hello", "created_at": "2026-05-15T10:30:00Z"}),
            json.dumps({"message_id": "msg-2", "recipient": "Bob", "channel": "push", "priority": "normal", "content": "update", "created_at": "2026-05-15T11:30:00Z"}),
        ]
    )

    monkeypatch.setattr("sys.stdin", StringIO(batch))
    code = main([])
    captured = capsys.readouterr()

    assert code == 0
    assert captured.err == ""
    lines = [json.loads(line) for line in captured.out.strip().splitlines()]
    assert lines == [
        {"message_id": "msg-1", "recipient": "Alice", "channel": "email", "priority": "high", "content": "hello", "created_at": "2026-05-15T10:30:00Z"},
        {"message_id": "msg-2", "recipient": "Bob", "channel": "push", "priority": "normal", "content": "update", "created_at": "2026-05-15T11:30:00Z"},
    ]
