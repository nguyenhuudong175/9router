from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pyrouter.storage.db import Database, json_dumps, json_loads


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class ComboRepo:
    def __init__(self, db: Database):
        self.db = db

    def list(self) -> list[dict]:
        rows = self.db.query_all("SELECT * FROM combos ORDER BY created_at ASC")
        return [
            {
                "id": r["id"],
                "name": r["name"],
                "kind": r["kind"],
                "models": json_loads(r["models_json"], []),
            }
            for r in rows
        ]

    def get_by_name(self, name: str) -> dict | None:
        row = self.db.query_one("SELECT * FROM combos WHERE name=?", (name,))
        if not row:
            return None
        return {
            "id": row["id"],
            "name": row["name"],
            "kind": row["kind"],
            "models": json_loads(row["models_json"], []),
        }

    def upsert(self, name: str, models: list[str], kind: str | None = None) -> dict:
        now = _now_iso()
        existing = self.get_by_name(name)
        combo_id = existing["id"] if existing else str(uuid4())
        self.db.execute(
            """
            INSERT INTO combos(id,name,kind,models_json,created_at,updated_at)
            VALUES(?,?,?,?,?,?)
            ON CONFLICT(name) DO UPDATE SET kind=excluded.kind,models_json=excluded.models_json,updated_at=excluded.updated_at
            """,
            (combo_id, name, kind, json_dumps(models), now, now),
        )
        return self.get_by_name(name)  # type: ignore[return-value]

