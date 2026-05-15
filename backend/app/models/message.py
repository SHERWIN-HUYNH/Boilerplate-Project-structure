from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ValidationError:
    field: str | None
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Message:
    message_id: str
    recipient: str
    channel: str
    priority: str
    content: str
    created_at: str


@dataclass(frozen=True, slots=True)
class NormalizedMessage:
    message_id: str
    recipient: str
    channel: str
    priority: str
    content: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "recipient": self.recipient,
            "channel": self.channel,
            "priority": self.priority,
            "content": self.content,
            "created_at": self.created_at,
        }
