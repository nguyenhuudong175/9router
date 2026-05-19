from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pyrouter.core.account_selector import AccountSelector
from pyrouter.core.chat_service import ChatService
from pyrouter.core.combo_router import ComboRouter
from pyrouter.core.fallback_policy import FallbackPolicy
from pyrouter.core.model_resolver import ModelResolver
from pyrouter.executors.registry import ExecutorRegistry
from pyrouter.storage.db import Database
from pyrouter.storage.repos import AliasRepo, ApiKeyRepo, ComboRepo, ConnectionRepo, SettingsRepo, UsageRepo
from pyrouter.translation.translator import Translator


def default_data_dir() -> Path:
    env = os.getenv("DATA_DIR")
    if env:
        return Path(env)
    return Path.home() / ".pyrouter"


@lru_cache(maxsize=1)
def get_db() -> Database:
    db_path = default_data_dir() / "db" / "data.sqlite"
    return Database(db_path)


@lru_cache(maxsize=1)
def get_chat_service() -> ChatService:
    db = get_db()
    settings = SettingsRepo(db)
    api_keys = ApiKeyRepo(db)
    connections = ConnectionRepo(db)
    aliases = AliasRepo(db)
    combos = ComboRepo(db)
    usage = UsageRepo(db)
    resolver = ModelResolver(aliases, combos)
    selector = AccountSelector(connections)
    combo_router = ComboRouter()
    fallback = FallbackPolicy()
    translator = Translator()
    executors = ExecutorRegistry()
    return ChatService(
        settings_repo=settings,
        api_key_repo=api_keys,
        connection_repo=connections,
        combo_repo=combos,
        resolver=resolver,
        account_selector=selector,
        combo_router=combo_router,
        fallback_policy=fallback,
        translator=translator,
        executor_registry=executors,
        usage_repo=usage,
    )

