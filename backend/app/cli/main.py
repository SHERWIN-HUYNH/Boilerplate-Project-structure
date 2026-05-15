from __future__ import annotations

import json
import sys

from app.ingestion.input_reader import detect_batch_mode, parse_jsonl, parse_single_json, read_text_source
from app.ingestion.normalizer import normalize_message
from app.ingestion.validator import validate_message


def _emit_error(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def _process_single(payload_text: str) -> tuple[int, str | None]:
    payload = parse_single_json(payload_text)
    message, error = validate_message(payload)
    if error:
        return 1, f"{error.field}: {error.message}"
    print(json.dumps(normalize_message(message).to_dict(), ensure_ascii=False))
    return 0, None


def _process_batch(payload_text: str) -> tuple[int, str | None]:
    for payload in parse_jsonl(payload_text):
        message, error = validate_message(payload)
        if error:
            return 1, f"{error.field}: {error.message}"
        print(json.dumps(normalize_message(message).to_dict(), ensure_ascii=False))
    return 0, None


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    argument = args[0] if args else None
    source_text = read_text_source(argument, sys.stdin.read() if argument is None else None)
    if not source_text.strip():
        return _emit_error("No input provided")

    try:
        if detect_batch_mode(source_text):
            code, error = _process_batch(source_text)
        else:
            code, error = _process_single(source_text)
        if error:
            return _emit_error(error)
        return code
    except Exception as exc:
        return _emit_error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
