from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pyrouter.storage.db import Database, json_dumps, json_loads


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _row_to_conn(row: Any) -> dict[str, Any]:
    data = json_loads(row["data_json"], {})
    return {
        "id": row["id"],
        "provider": row["provider"],
        "auth_type": row["auth_type"],
        "name": row["name"],
        "priority": row["priority"] or 1,
        "is_active": bool(row["is_active"]),
        "api_key": row["api_key"],
        "access_token": row["access_token"],
        "refresh_token": row["refresh_token"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        **data,
    }


class ConnectionRepo:
    def __init__(self, db: Database):
        self.db = db

    def list_active(self, provider: str | None = None) -> list[dict[str, Any]]:
        if provider:
            rows = self.db.query_all(
                "SELECT * FROM provider_connections WHERE is_active=1 AND provider=? ORDER BY priority ASC, updated_at DESC",
                (provider,),
            )
        else:
            rows = self.db.query_all(
                "SELECT * FROM provider_connections WHERE is_active=1 ORDER BY provider ASC, priority ASC"
            )
        return [_row_to_conn(r) for r in rows]

    def get_by_id(self, connection_id: str) -> dict[str, Any] | None:
        row = self.db.query_one("SELECT * FROM provider_connections WHERE id=?", (connection_id,))
        return _row_to_conn(row) if row else None

    def upsert(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = _now_iso()
        connection_id = payload.get("id") or str(uuid4())
        existing = self.get_by_id(connection_id)
        base = existing or {}
        merged = {**base, **payload}
        data = {
            k: v
            for k, v in merged.items()
            if k
            not in {
                "id",
                "provider",
                "auth_type",
                "name",
                "priority",
                "is_active",
                "api_key",
                "access_token",
                "refresh_token",
                "created_at",
                "updated_at",
            }
        }
        self.db.execute(
            """
            INSERT INTO provider_connections(
              id,provider,auth_type,name,priority,is_active,api_key,access_token,refresh_token,data_json,created_at,updated_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
              provider=excluded.provider,auth_type=excluded.auth_type,name=excluded.name,priority=excluded.priority,
              is_active=excluded.is_active,api_key=excluded.api_key,access_token=excluded.access_token,refresh_token=excluded.refresh_token,
              data_json=excluded.data_json,updated_at=excluded.updated_at
            """,
            (
                connection_id,
                merged["provider"],
                merged.get("auth_type", "apikey"),
                merged.get("name"),
                merged.get("priority", 1),
                1 if merged.get("is_active", True) else 0,
                merged.get("api_key"),
                merged.get("access_token"),
                merged.get("refresh_token"),
                json_dumps(data),
                merged.get("created_at", now),
                now,
            ),
        )
        return self.get_by_id(connection_id)  # type: ignore[return-value]

    def update_state(self, connection_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        current = self.get_by_id(connection_id)
        if not current:
            return None
        merged = {**current, **updates}
        return self.upsert(merged)

