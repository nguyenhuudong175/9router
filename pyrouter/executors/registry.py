from __future__ import annotations

from pyrouter.executors.base import Executor
from pyrouter.executors.claude_compat import ClaudeCompatibleExecutor
from pyrouter.executors.openai_compat import OpenAICompatibleExecutor


class ExecutorRegistry:
    def __init__(self):
        self.default_openai = OpenAICompatibleExecutor()
        self.default_claude = ClaudeCompatibleExecutor()
        self._custom: dict[str, Executor] = {}

    def register(self, provider: str, executor: Executor) -> None:
        self._custom[provider] = executor

    def get(self, provider: str, target_format: str) -> Executor:
        if provider in self._custom:
            return self._custom[provider]
        if target_format == "claude":
            return self.default_claude
        return self.default_openai

