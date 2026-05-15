from __future__ import annotations

from app.ingestion.normalizer import normalize_message
from app.ingestion.validator import validate_message


def test_validate_message_accepts_required_fields_and_normalizes_whitespace():
    payload = {
        "message_id": " msg-1 ",
        "recipient": " Alice ",
        "channel": "EMAIL",
        "priority": "High",
        "content": " hello ",
        "created_at": "2026-05-15T10:30:00Z",
    }

    message, error = validate_message(payload)

    assert error is None
    assert message is not None
    normalized = normalize_message(message)
    assert normalized.to_dict() == {
        "message_id": "msg-1",
        "recipient": "Alice",
        "channel": "email",
        "priority": "high",
        "content": "hello",
        "created_at": "2026-05-15T10:30:00Z",
    }


def test_validate_message_rejects_missing_field():
    payload = {
        "message_id": "msg-1",
        "recipient": "Alice",
        "channel": "email",
        "priority": "high",
        "content": "hello",
    }

    message, error = validate_message(payload)

    assert message is None
    assert error is not None
    assert error.field == "created_at"
    assert error.code == "missing_field"


def test_validate_message_rejects_invalid_enum_value():
    payload = {
        "message_id": "msg-1",
        "recipient": "Alice",
        "channel": "fax",
        "priority": "high",
        "content": "hello",
        "created_at": "2026-05-15T10:30:00Z",
    }

    message, error = validate_message(payload)

    assert message is None
    assert error is not None
    assert error.field == "channel"
    assert error.code == "invalid_enum"
