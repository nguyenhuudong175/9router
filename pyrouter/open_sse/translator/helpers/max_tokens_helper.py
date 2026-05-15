from pyrouter.open_sse.config.runtime_config import DEFAULT_MAX_TOKENS, DEFAULT_MIN_TOKENS


def adjust_max_tokens(body: dict) -> int:
    max_tokens = body.get("max_tokens") or DEFAULT_MAX_TOKENS

    if body.get("tools") and isinstance(body.get("tools"), list):
        if max_tokens < DEFAULT_MIN_TOKENS:
            max_tokens = DEFAULT_MIN_TOKENS

    thinking = body.get("thinking") or {}
    budget_tokens = thinking.get("budget_tokens")
    if budget_tokens and max_tokens <= budget_tokens:
        max_tokens = budget_tokens + 1024

    return max_tokens
