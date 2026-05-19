from __future__ import annotations

from typing import Any

from pyrouter.storage.db import Database, json_dumps, json_loads


DEFAULT_SETTINGS: dict[str, Any] = {
    "require_api_key": False,
    "fallback_strategy": "fill-first",
    "combo_strategy": "fallback",
    "combo_sticky_limit": 1,
}


class SettingsRepo:
    def __init__(self, db: Database):
        self.db = db

    def get(self) -> dict[str, Any]:
        row = self.db.query_one("SELECT data FROM settings WHERE id=1")
        data = json_loads(row["data"] if row else "{}", {})
        merged = dict(DEFAULT_SETTINGS)
        merged.update(data)
        return merged

    def update(self, updates: dict[str, Any]) -> dict[str, Any]:
        next_settings = self.get()
        next_settings.update(updates)
        self.db.execute(
            "INSERT INTO settings(id,data) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data",
            (json_dumps(next_settings),),
        )
        return next_settings

