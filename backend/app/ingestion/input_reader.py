from __future__ import annotations

import json
from pathlib import Path


def read_text_source(argument: str | None, stdin_text: str | None = None) -> str:
    if argument is None:
        return stdin_text or ""

    candidate = Path(argument)
    if candidate.exists() and candidate.is_file():
        return candidate.read_text(encoding="utf-8")

    return argument


def parse_single_json(text: str) -> dict[str, object]:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Single JSON input must be an object")
    return data


def parse_jsonl(text: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        data = json.loads(stripped)
        if not isinstance(data, dict):
            raise ValueError("JSONL input must contain JSON objects")
        records.append(data)
    return records


def detect_batch_mode(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return len(lines) > 1
