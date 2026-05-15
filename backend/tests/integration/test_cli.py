from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

from app.cli.main import main


def run_cli(monkeypatch, capsys, argv, stdin_text=None):
    monkeypatch.setattr("sys.stdin", StringIO(stdin_text or ""))
    code = main(argv)
    captured = capsys.readouterr()
    return code, captured


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

    code, captured = run_cli(monkeypatch, capsys, [payload])

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

    code, captured = run_cli(monkeypatch, capsys, [str(batch)])

    assert code == 0
    assert captured.err == ""
    lines = [json.loads(line) for line in captured.out.strip().splitlines()]
    assert lines == [
        {"message_id": "msg-1", "recipient": "Alice", "channel": "email", "priority": "high", "content": "hello", "created_at": "2026-05-15T10:30:00Z"},
        {"message_id": "msg-2", "recipient": "Bob", "channel": "sms", "priority": "low", "content": "ping", "created_at": "2026-05-15T11:30:00Z"},
    ]


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

    code, captured = run_cli(monkeypatch, capsys, [payload])

    assert code == 1
    assert captured.out == ""
    assert "channel" in captured.err
