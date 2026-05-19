from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pyrouter.storage.db import Database


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class ApiKeyRepo:
    def __init__(self, db: Database):
        self.db = db

    def create(self, key: str, name: str | None = None) -> dict:
        row_id = str(uuid4())
        self.db.execute(
            "INSERT INTO api_keys(id,name,key,is_active,created_at) VALUES(?,?,?,?,?)",
            (row_id, name, key, 1, _now_iso()),
        )
        return {"id": row_id, "key": key, "name": name, "is_active": True}

    def is_valid(self, key: str | None) -> bool:
        if not key:
            return False
        row = self.db.query_one("SELECT id FROM api_keys WHERE key=? AND is_active=1", (key,))
        return bool(row)

