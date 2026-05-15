from __future__ import annotations

from app.models.message import Message, ValidationError

REQUIRED_FIELDS = ("message_id", "recipient", "channel", "priority", "content", "created_at")
ALLOWED_CHANNELS = {"email", "sms", "push"}
ALLOWED_PRIORITIES = {"high", "normal", "low"}


def _as_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def validate_message(payload: dict[str, object]) -> tuple[Message | None, ValidationError | None]:
    for field in REQUIRED_FIELDS:
        if field not in payload:
            return None, ValidationError(field=field, code="missing_field", message=f"Missing required field: {field}")

    message_id = _as_text(payload["message_id"])
    recipient = _as_text(payload["recipient"])
    channel = _as_text(payload["channel"])
    priority = _as_text(payload["priority"])
    content = _as_text(payload["content"])
    created_at = _as_text(payload["created_at"])

    for field, value in (
        ("message_id", message_id),
        ("recipient", recipient),
        ("content", content),
        ("created_at", created_at),
    ):
        if not value:
            return None, ValidationError(field=field, code="invalid_format", message=f"Field '{field}' must not be empty")

    if channel.lower() not in ALLOWED_CHANNELS:
        return None, ValidationError(field="channel", code="invalid_enum", message=f"Invalid channel: {channel}")
    if priority.lower() not in ALLOWED_PRIORITIES:
        return None, ValidationError(field="priority", code="invalid_enum", message=f"Invalid priority: {priority}")

    return Message(
        message_id=message_id,
        recipient=recipient,
        channel=channel,
        priority=priority,
        content=content,
        created_at=created_at,
    ), None
