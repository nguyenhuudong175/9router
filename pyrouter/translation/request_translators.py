from __future__ import annotations

from copy import deepcopy
from typing import Any


def _claude_message_to_openai(msg: dict[str, Any]) -> dict[str, Any]:
    content = msg.get("content", "")
    if isinstance(content, list):
        text_parts = [p.get("text", "") for p in content if p.get("type") == "text"]
        content = "\n".join([p for p in text_parts if p])
    return {"role": msg.get("role", "user"), "content": content}


def _openai_message_to_claude(msg: dict[str, Any]) -> dict[str, Any]:
    content = msg.get("content", "")
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]
    return {"role": msg.get("role", "user"), "content": content}


def translate_request(source_format: str, target_format: str, body: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(body)
    if source_format == target_format:
        return payload

    if source_format == "openai-responses":
        inp = payload.get("input", "")
        if isinstance(inp, str):
            payload = {"messages": [{"role": "user", "content": inp}], "stream": payload.get("stream", False)}
        elif isinstance(inp, list):
            payload = {"messages": inp, "stream": payload.get("stream", False)}
        source_format = "openai"

    if source_format == "claude" and target_format == "openai":
        messages = payload.get("messages", [])
        payload["messages"] = [_claude_message_to_openai(m) for m in messages]
        payload.pop("anthropic_version", None)
        return payload

    if source_format == "openai" and target_format == "claude":
        messages = payload.get("messages", [])
        payload["messages"] = [_openai_message_to_claude(m) for m in messages]
        payload["anthropic_version"] = "2023-06-01"
        return payload

    return payload

