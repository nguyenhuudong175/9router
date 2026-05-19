from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass
class FallbackDecision:
    should_fallback: bool
    cooldown_seconds: int
    new_backoff_level: int


class FallbackPolicy:
    def __init__(self, base_backoff_seconds: int = 2, max_backoff_seconds: int = 300) -> None:
        self.base_backoff_seconds = base_backoff_seconds
        self.max_backoff_seconds = max_backoff_seconds

    def classify(self, status: int, message: str, backoff_level: int = 0) -> FallbackDecision:
        text = (message or "").lower()
        if status == 429 or "rate limit" in text or "quota" in text:
            level = min(backoff_level + 1, 15)
            cooldown = min(self.base_backoff_seconds * (2 ** max(level - 1, 0)), self.max_backoff_seconds)
            return FallbackDecision(True, cooldown, level)
        if status in {401, 402, 403, 404}:
            return FallbackDecision(True, 120, backoff_level)
        if status >= 500 or status == 0:
            return FallbackDecision(True, 30, backoff_level)
        return FallbackDecision(False, 0, backoff_level)

    @staticmethod
    def lock_until(cooldown_seconds: int) -> str:
        return (datetime.now(UTC) + timedelta(seconds=cooldown_seconds)).isoformat()

