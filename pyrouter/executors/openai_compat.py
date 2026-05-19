from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .base import ExecutionResult, Executor


class OpenAICompatibleExecutor(Executor):
    target_format = "openai"

    def execute(self, model: str, payload: dict[str, Any], stream: bool, credentials: dict[str, Any]) -> ExecutionResult:
        base_url = credentials.get("base_url", "https://api.openai.com/v1/chat/completions").rstrip("/")
        if base_url.endswith("/v1"):
            url = f"{base_url}/chat/completions"
        else:
            url = base_url
        body = dict(payload)
        body["model"] = model
        api_key = credentials.get("api_key") or credentials.get("access_token")
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        req = Request(url=url, method="POST", data=json.dumps(body).encode("utf-8"), headers=headers)
        try:
            with urlopen(req, timeout=30) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
                return ExecutionResult(ok=True, status=resp.status, body=parsed)
        except HTTPError as e:
            text = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
            return ExecutionResult(ok=False, status=e.code, error=text)
        except URLError as e:
            return ExecutionResult(ok=False, status=502, error=str(e))

