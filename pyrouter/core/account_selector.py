from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pyrouter.core.fallback_policy import FallbackDecision, FallbackPolicy
from pyrouter.storage.repos import ConnectionRepo


class AccountSelector:
    def __init__(self, connection_repo: ConnectionRepo):
        self.connection_repo = connection_repo

    def select(self, provider: str, model: str, excluded_ids: set[str] | None = None) -> dict[str, Any] | None:
        excluded = excluded_ids or set()
        now = datetime.now(UTC)
        for conn in self.connection_repo.list_active(provider):
            if conn["id"] in excluded:
                continue
            locks = conn.get("model_locks", {}) or {}
            lock_until = locks.get(model) or locks.get("__all")
            if lock_until:
                try:
                    if datetime.fromisoformat(lock_until) > now:
                        continue
                except ValueError:
                    pass
            return conn
        return None

    def mark_unavailable(
        self,
        connection_id: str,
        model: str,
        decision: FallbackDecision,
        status: int,
        error: str,
    ) -> None:
        conn = self.connection_repo.get_by_id(connection_id)
        if not conn:
            return
        locks = dict(conn.get("model_locks", {}) or {})
        locks[model] = FallbackPolicy.lock_until(decision.cooldown_seconds)
        self.connection_repo.update_state(
            connection_id,
            {
                "model_locks": locks,
                "last_error": (error or "")[:300],
                "error_code": status,
                "backoff_level": decision.new_backoff_level,
            },
        )

    def clear_success(self, connection_id: str, model: str) -> None:
        conn = self.connection_repo.get_by_id(connection_id)
        if not conn:
            return
        locks = dict(conn.get("model_locks", {}) or {})
        locks.pop(model, None)
        self.connection_repo.update_state(
            connection_id,
            {
                "model_locks": locks,
                "last_error": None,
                "error_code": None,
                "backoff_level": 0,
            },
        )

