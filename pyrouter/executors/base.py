from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionResult:
    ok: bool
    status: int
    body: dict[str, Any] | None = None
    error: str | None = None


class Executor:
    target_format = "openai"

    def execute(self, model: str, payload: dict[str, Any], stream: bool, credentials: dict[str, Any]) -> ExecutionResult:
        raise NotImplementedError

