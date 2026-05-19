from __future__ import annotations

from typing import Any


def detect_format(body: dict[str, Any]) -> str:
    if "input" in body and "messages" not in body:
        return "openai-responses"
    if body.get("anthropic_version") or body.get("system") and isinstance(body.get("messages"), list):
        first = body["messages"][0] if body["messages"] else {}
        if isinstance(first.get("content"), list):
            return "claude"
    if "messages" in body:
        return "openai"
    return "openai"

