from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .base import ExecutionResult, Executor


class ClaudeCompatibleExecutor(Executor):
    target_format = "claude"

    def execute(self, model: str, payload: dict, stream: bool, credentials: dict) -> ExecutionResult:
        base_url = credentials.get("base_url", "https://api.anthropic.com/v1/messages").rstrip("/")
        if base_url.endswith("/v1"):
            url = f"{base_url}/messages"
        else:
            url = base_url
        body = dict(payload)
        body["model"] = model
        api_key = credentials.get("api_key") or credentials.get("access_token")
        headers = {"Content-Type": "application/json", "anthropic-version": "2023-06-01"}
        if api_key:
            headers["x-api-key"] = api_key
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

