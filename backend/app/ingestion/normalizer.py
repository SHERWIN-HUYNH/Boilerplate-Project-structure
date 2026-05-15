from __future__ import annotations

from datetime import datetime, timezone

from app.models.message import Message, NormalizedMessage


def _normalize_timestamp(value: str) -> str:
    candidate = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(candidate)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_message(message: Message) -> NormalizedMessage:
    return NormalizedMessage(
        message_id=message.message_id,
        recipient=message.recipient.strip(),
        channel=message.channel.strip().lower(),
        priority=message.priority.strip().lower(),
        content=message.content.strip(),
        created_at=_normalize_timestamp(message.created_at.strip()),
    )
