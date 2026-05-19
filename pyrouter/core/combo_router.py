from __future__ import annotations

from collections import defaultdict


class ComboRouter:
    def __init__(self) -> None:
        self._state: dict[str, dict[str, int]] = defaultdict(lambda: {"index": 0, "count": 0})

    def route(self, models: list[str], combo_name: str, strategy: str, sticky_limit: int = 1) -> list[str]:
        if strategy != "round-robin" or len(models) <= 1:
            return list(models)
        sticky = max(1, int(sticky_limit or 1))
        state = self._state[combo_name or "__default__"]
        idx = state["index"] % len(models)
        ordered = models[idx:] + models[:idx]
        state["count"] += 1
        if state["count"] >= sticky:
            state["index"] = (idx + 1) % len(models)
            state["count"] = 0
        else:
            state["index"] = idx
        return ordered

    def reset(self, combo_name: str | None = None) -> None:
        if combo_name:
            self._state.pop(combo_name, None)
            return
        self._state.clear()

