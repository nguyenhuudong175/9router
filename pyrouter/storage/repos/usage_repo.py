from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pyrouter.storage.db import Database, json_dumps, json_loads


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class UsageRepo:
    def __init__(self, db: Database):
        self.db = db

    def add_usage(
        self,
        provider: str,
        model: str,
        connection_id: str | None,
        status: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cost: float = 0.0,
        meta: dict[str, Any] | None = None,
    ) -> None:
        self.db.execute(
            """
            INSERT INTO usage_history(
              timestamp,provider,model,connection_id,status,prompt_tokens,completion_tokens,total_tokens,cost,meta_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                _now_iso(),
                provider,
                model,
                connection_id,
                status,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                cost,
                json_dumps(meta or {}),
            ),
        )

    def append_log(self, status: str, provider: str | None, model: str | None, connection_id: str | None, message: str) -> None:
        self.db.execute(
            """
            INSERT INTO request_logs(timestamp,status,provider,model,connection_id,message)
            VALUES(?,?,?,?,?,?)
            """,
            (_now_iso(), status, provider, model, connection_id, message),
        )

    def recent_usage(self, limit: int = 20) -> list[dict]:
        rows = self.db.query_all("SELECT * FROM usage_history ORDER BY id DESC LIMIT ?", (limit,))
        return [
            {
                "provider": r["provider"],
                "model": r["model"],
                "status": r["status"],
                "prompt_tokens": r["prompt_tokens"],
                "completion_tokens": r["completion_tokens"],
                "total_tokens": r["total_tokens"],
                "meta": json_loads(r["meta_json"], {}),
            }
            for r in rows
        ]

