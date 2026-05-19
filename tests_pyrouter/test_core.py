import tempfile
import unittest
from pathlib import Path

from pyrouter.core.account_selector import AccountSelector
from pyrouter.core.combo_router import ComboRouter
from pyrouter.core.fallback_policy import FallbackPolicy
from pyrouter.core.model_resolver import ModelResolver
from pyrouter.storage.db import Database
from pyrouter.storage.repos import AliasRepo, ComboRepo, ConnectionRepo


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.tmp.name) / "db.sqlite")
        self.alias_repo = AliasRepo(self.db)
        self.combo_repo = ComboRepo(self.db)
        self.connection_repo = ConnectionRepo(self.db)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_model_resolution_direct_alias_combo(self):
        self.alias_repo.set("prod", "openai/gpt-4o")
        self.combo_repo.upsert("coding", ["prod", "anthropic/claude-sonnet-4"])
        resolver = ModelResolver(self.alias_repo, self.combo_repo)

        one = resolver.resolve("openai/gpt-4.1")
        self.assertFalse(one.is_combo)
        self.assertEqual(one.candidates[0].provider, "openai")

        alias = resolver.resolve("prod")
        self.assertEqual(alias.candidates[0].model, "gpt-4o")

        combo = resolver.resolve("coding")
        self.assertTrue(combo.is_combo)
        self.assertEqual(len(combo.candidates), 2)

    def test_combo_sticky_round_robin(self):
        router = ComboRouter()
        models = ["a/m1", "b/m2"]
        picks = [router.route(models, "combo1", "round-robin", 2)[0] for _ in range(6)]
        self.assertEqual(picks, ["a/m1", "a/m1", "b/m2", "b/m2", "a/m1", "a/m1"])

    def test_account_selector_skips_locked_and_excluded(self):
        self.connection_repo.upsert({"id": "c1", "provider": "openai", "api_key": "k1", "priority": 1, "model_locks": {"gpt-4o": "2999-01-01T00:00:00+00:00"}})
        self.connection_repo.upsert({"id": "c2", "provider": "openai", "api_key": "k2", "priority": 2})
        selector = AccountSelector(self.connection_repo)
        selected = selector.select("openai", "gpt-4o", excluded_ids={"c2"})
        self.assertIsNone(selected)
        selected2 = selector.select("openai", "gpt-4o", excluded_ids=set())
        self.assertEqual(selected2["id"], "c2")

    def test_fallback_classification(self):
        policy = FallbackPolicy()
        d1 = policy.classify(429, "rate limit", 0)
        self.assertTrue(d1.should_fallback)
        self.assertGreaterEqual(d1.cooldown_seconds, 2)
        d2 = policy.classify(401, "unauthorized", 0)
        self.assertEqual(d2.cooldown_seconds, 120)
        d3 = policy.classify(400, "bad request", 0)
        self.assertFalse(d3.should_fallback)


if __name__ == "__main__":
    unittest.main()

