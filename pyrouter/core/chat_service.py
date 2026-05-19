from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from pyrouter.core.account_selector import AccountSelector
from pyrouter.core.combo_router import ComboRouter
from pyrouter.core.fallback_policy import FallbackPolicy
from pyrouter.core.model_resolver import ModelResolver
from pyrouter.executors.registry import ExecutorRegistry
from pyrouter.storage.repos import ApiKeyRepo, ComboRepo, ConnectionRepo, SettingsRepo, UsageRepo
from pyrouter.translation.translator import Translator
from pyrouter.usage.tracker import UsageTracker


@dataclass
class ChatResult:
    status: int
    body: dict[str, Any]


class ChatService:
    def __init__(
        self,
        settings_repo: SettingsRepo,
        api_key_repo: ApiKeyRepo,
        connection_repo: ConnectionRepo,
        combo_repo: ComboRepo,
        resolver: ModelResolver,
        account_selector: AccountSelector,
        combo_router: ComboRouter,
        fallback_policy: FallbackPolicy,
        translator: Translator,
        executor_registry: ExecutorRegistry,
        usage_repo: UsageRepo,
    ):
        self.settings_repo = settings_repo
        self.api_key_repo = api_key_repo
        self.connection_repo = connection_repo
        self.combo_repo = combo_repo
        self.resolver = resolver
        self.account_selector = account_selector
        self.combo_router = combo_router
        self.fallback_policy = fallback_policy
        self.translator = translator
        self.executor_registry = executor_registry
        self.usage_repo = usage_repo

    def _auth_check(self, headers: dict[str, str]) -> ChatResult | None:
        settings = self.settings_repo.get()
        if not settings.get("require_api_key", False):
            return None
        auth = headers.get("authorization", "")
        key = auth[7:] if auth.lower().startswith("bearer ") else headers.get("x-api-key")
        if not self.api_key_repo.is_valid(key):
            return ChatResult(status=401, body={"error": {"message": "Invalid API key"}})
        return None

    def _provider_target_format(self, connection: dict[str, Any]) -> str:
        target = connection.get("target_format")
        if target:
            return target
        provider = connection.get("provider", "")
        if "claude" in provider or "anthropic" in provider:
            return "claude"
        return "openai"

    def handle_chat(self, request_body: dict[str, Any], headers: dict[str, str] | None = None) -> ChatResult:
        headers = {k.lower(): v for k, v in (headers or {}).items()}
        auth_error = self._auth_check(headers)
        if auth_error:
            return auth_error

        model = request_body.get("model")
        if not model:
            return ChatResult(status=400, body={"error": {"message": "Missing model"}})

        source_fmt = self.translator.detect_format(request_body)
        resolved = self.resolver.resolve(model)
        settings = self.settings_repo.get()
        candidates = resolved.candidates
        if resolved.is_combo and candidates:
            ordered_raw = [f"{c.provider}/{c.model}" for c in candidates]
            ordered = self.combo_router.route(
                ordered_raw,
                resolved.candidates[0].combo_name or model,
                settings.get("combo_strategy", "fallback"),
                settings.get("combo_sticky_limit", 1),
            )
            map_raw = {f"{c.provider}/{c.model}": c for c in candidates}
            candidates = [map_raw[r] for r in ordered]

        last_error = "All candidates unavailable"
        last_status = 503
        for candidate in candidates:
            excluded: set[str] = set()
            while True:
                connection = self.account_selector.select(candidate.provider, candidate.model, excluded)
                if not connection:
                    break

                target_fmt = self._provider_target_format(connection)
                payload = self.translator.translate_request(source_fmt, target_fmt, request_body)
                executor = self.executor_registry.get(candidate.provider, target_fmt)
                result = executor.execute(
                    model=candidate.model,
                    payload=payload,
                    stream=bool(request_body.get("stream", False)),
                    credentials=connection,
                )

                if result.ok and result.body is not None:
                    self.account_selector.clear_success(connection["id"], candidate.model)
                    normalized = self.translator.translate_response(target_fmt, source_fmt, result.body)
                    usage = UsageTracker.extract_or_estimate(result.body, request_body)
                    self.usage_repo.add_usage(
                        provider=candidate.provider,
                        model=candidate.model,
                        connection_id=connection["id"],
                        status="200 OK",
                        prompt_tokens=usage["prompt_tokens"],
                        completion_tokens=usage["completion_tokens"],
                        total_tokens=usage["total_tokens"],
                        meta={"source_format": source_fmt, "target_format": target_fmt},
                    )
                    self.usage_repo.append_log(
                        status="200 OK",
                        provider=candidate.provider,
                        model=candidate.model,
                        connection_id=connection["id"],
                        message="success",
                    )
                    return ChatResult(status=200, body=normalized)

                status = result.status
                error = result.error or "Upstream error"
                decision = self.fallback_policy.classify(status, error, int(connection.get("backoff_level", 0) or 0))
                if decision.should_fallback:
                    self.account_selector.mark_unavailable(connection["id"], candidate.model, decision, status, error)
                    excluded.add(connection["id"])
                    last_error = error
                    last_status = status
                    self.usage_repo.append_log(
                        status=f"FAILED {status}",
                        provider=candidate.provider,
                        model=candidate.model,
                        connection_id=connection["id"],
                        message=error[:300],
                    )
                    continue

                return ChatResult(status=status, body={"error": {"message": error}})

        return ChatResult(status=last_status, body={"error": {"message": last_error}})

    def list_models(self) -> dict[str, Any]:
        data: list[dict[str, Any]] = []
        for combo in self.combo_repo.list():
            data.append({"id": combo["name"], "object": "model", "owned_by": "combo"})
        for conn in self.connection_repo.list_active():
            alias = conn.get("prefix") or conn["provider"]
            default_model = conn.get("default_model") or "default"
            data.append({"id": f"{alias}/{default_model}", "object": "model", "owned_by": alias})
        deduped = []
        seen = set()
        for item in data:
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            deduped.append(item)
        return {"object": "list", "data": deduped}

