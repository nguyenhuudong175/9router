import tempfile
import unittest
from pathlib import Path

from pyrouter.core.account_selector import AccountSelector
from pyrouter.core.chat_service import ChatService
from pyrouter.core.combo_router import ComboRouter
from pyrouter.core.fallback_policy import FallbackPolicy
from pyrouter.core.model_resolver import ModelResolver
from pyrouter.executors.base import ExecutionResult, Executor
from pyrouter.executors.registry import ExecutorRegistry
from pyrouter.storage.db import Database
from pyrouter.storage.repos import AliasRepo, ApiKeyRepo, ComboRepo, ConnectionRepo, SettingsRepo, UsageRepo
from pyrouter.translation.translator import Translator


class FakeExecutor(Executor):
    def __init__(self, responses):
        self.responses = list(responses)
        self.target_format = "openai"

    def execute(self, model, payload, stream, credentials):
        return self.responses.pop(0)


class ChatServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.tmp.name) / "db.sqlite")
        self.settings = SettingsRepo(self.db)
        self.keys = ApiKeyRepo(self.db)
        self.connections = ConnectionRepo(self.db)
        self.aliases = AliasRepo(self.db)
        self.combos = ComboRepo(self.db)
        self.usage = UsageRepo(self.db)
        self.resolver = ModelResolver(self.aliases, self.combos)
        self.selector = AccountSelector(self.connections)
        self.combo_router = ComboRouter()
        self.fallback = FallbackPolicy()
        self.registry = ExecutorRegistry()
        self.service = ChatService(
            settings_repo=self.settings,
            api_key_repo=self.keys,
            connection_repo=self.connections,
            combo_repo=self.combos,
            resolver=self.resolver,
            account_selector=self.selector,
            combo_router=self.combo_router,
            fallback_policy=self.fallback,
            translator=Translator(),
            executor_registry=self.registry,
            usage_repo=self.usage,
        )
        self.connections.upsert({"id": "c1", "provider": "openai", "api_key": "k1", "prefix": "openai", "default_model": "gpt-4o"})
        self.connections.upsert({"id": "c2", "provider": "anthropic", "api_key": "k2", "prefix": "anthropic", "default_model": "claude-sonnet-4"})

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_happy_path_returns_openai_shape(self):
        self.registry.register(
            "openai",
            FakeExecutor([ExecutionResult(ok=True, status=200, body={"id": "x", "object": "chat.completion", "choices": [{"index": 0, "message": {"role": "assistant", "content": "hi"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7}})]),
        )
        result = self.service.handle_chat({"model": "openai/gpt-4o", "messages": [{"role": "user", "content": "hello"}]})
        self.assertEqual(result.status, 200)
        self.assertEqual(result.body["choices"][0]["message"]["content"], "hi")

    def test_fallback_switches_to_next_combo_model(self):
        self.combos.upsert("mix", ["openai/gpt-4o", "anthropic/claude-sonnet-4"])
        self.registry.register(
            "openai",
            FakeExecutor([ExecutionResult(ok=False, status=429, error="rate limit")]),
        )
        self.registry.register(
            "anthropic",
            FakeExecutor([ExecutionResult(ok=True, status=200, body={"id": "m1", "content": [{"type": "text", "text": "fallback ok"}], "usage": {"input_tokens": 2, "output_tokens": 1}})]),
        )
        result = self.service.handle_chat({"model": "mix", "messages": [{"role": "user", "content": "hello"}]})
        self.assertEqual(result.status, 200)
        self.assertEqual(result.body["choices"][0]["message"]["content"], "fallback ok")

    def test_models_list_contains_combo_and_provider_models(self):
        self.combos.upsert("coding", ["openai/gpt-4o"])
        out = self.service.list_models()
        ids = {m["id"] for m in out["data"]}
        self.assertIn("coding", ids)
        self.assertIn("openai/gpt-4o", ids)

    def test_usage_estimation_when_missing_provider_usage(self):
        self.registry.register(
            "openai",
            FakeExecutor([ExecutionResult(ok=True, status=200, body={"id": "x", "object": "chat.completion", "choices": [{"index": 0, "message": {"role": "assistant", "content": "text"}, "finish_reason": "stop"}]})]),
        )
        result = self.service.handle_chat({"model": "openai/gpt-4o", "messages": [{"role": "user", "content": "hello"}]})
        self.assertEqual(result.status, 200)
        usage = self.usage.recent_usage(1)[0]
        self.assertGreater(usage["total_tokens"], 0)


if __name__ == "__main__":
    unittest.main()
