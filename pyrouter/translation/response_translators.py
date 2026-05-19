from __future__ import annotations

from copy import deepcopy
from typing import Any


def translate_response(source_format: str, target_format: str, body: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(body)
    if source_format == target_format:
        return payload

    if source_format == "claude" and target_format == "openai":
        content_blocks = payload.get("content", [])
        text = "".join([b.get("text", "") for b in content_blocks if b.get("type") == "text"])
        usage = payload.get("usage", {})
        return {
            "id": f"chatcmpl-{payload.get('id', 'mvp')}",
            "object": "chat.completion",
            "model": payload.get("model", "claude"),
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            },
        }

    if source_format == "openai" and target_format == "claude":
        msg = payload.get("choices", [{}])[0].get("message", {})
        return {
            "id": payload.get("id", "msg_mvp"),
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": msg.get("content", "")}],
        }

    return payload

