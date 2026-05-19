from __future__ import annotations

import json
from typing import Any


class UsageTracker:
    @staticmethod
    def extract_or_estimate(response_body: dict[str, Any], request_body: dict[str, Any]) -> dict[str, int]:
        usage = response_body.get("usage")
        if isinstance(usage, dict):
            prompt = int(usage.get("prompt_tokens", usage.get("input_tokens", 0)) or 0)
            completion = int(usage.get("completion_tokens", usage.get("output_tokens", 0)) or 0)
            total = int(usage.get("total_tokens", prompt + completion) or prompt + completion)
            return {"prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": total}

        req_chars = len(json.dumps(request_body, ensure_ascii=False))
        out_chars = len(json.dumps(response_body, ensure_ascii=False))
        prompt = max(1, req_chars // 4)
        completion = max(1, out_chars // 4)
        return {"prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": prompt + completion}

