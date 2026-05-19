from __future__ import annotations

from dataclasses import dataclass

from pyrouter.storage.repos import AliasRepo, ComboRepo


@dataclass
class ModelCandidate:
    provider: str
    model: str
    combo_name: str | None = None


@dataclass
class ResolveResult:
    is_combo: bool
    candidates: list[ModelCandidate]


class ModelResolver:
    def __init__(self, alias_repo: AliasRepo, combo_repo: ComboRepo):
        self.alias_repo = alias_repo
        self.combo_repo = combo_repo

    @staticmethod
    def _split_model(model_str: str) -> tuple[str, str]:
        if "/" in model_str:
            p, m = model_str.split("/", 1)
            return p, m
        return "openai", model_str

    def resolve(self, model_str: str) -> ResolveResult:
        combo = self.combo_repo.get_by_name(model_str)
        if combo:
            candidates: list[ModelCandidate] = []
            for item in combo["models"]:
                provider, model = self._resolve_alias_or_direct(item)
                candidates.append(ModelCandidate(provider=provider, model=model, combo_name=combo["name"]))
            return ResolveResult(is_combo=True, candidates=candidates)
        provider, model = self._resolve_alias_or_direct(model_str)
        return ResolveResult(is_combo=False, candidates=[ModelCandidate(provider=provider, model=model)])

    def _resolve_alias_or_direct(self, model_str: str) -> tuple[str, str]:
        aliases = self.alias_repo.get_all()
        mapped = aliases.get(model_str, model_str)
        return self._split_model(mapped)

