from __future__ import annotations

from pyrouter.storage.db import Database


class AliasRepo:
    def __init__(self, db: Database):
        self.db = db

    def get_all(self) -> dict[str, str]:
        rows = self.db.query_all("SELECT alias,target_model FROM model_aliases")
        return {r["alias"]: r["target_model"] for r in rows}

    def set(self, alias: str, target_model: str) -> None:
        self.db.execute(
            "INSERT INTO model_aliases(alias,target_model) VALUES(?,?) ON CONFLICT(alias) DO UPDATE SET target_model=excluded.target_model",
            (alias, target_model),
        )

    def delete(self, alias: str) -> None:
        self.db.execute("DELETE FROM model_aliases WHERE alias=?", (alias,))

