from .openai import create_openai_embedding_adapter
from .openai_compat_node import openai_compat_node

OPENAI_COMPAT_PROVIDERS = [
    "openai",
    "openrouter",
    "mistral",
    "voyage-ai",
    "fireworks",
    "together",
    "nebius",
    "github",
    "nvidia",
    "jina-ai",
]

ADAPTERS = {provider: create_openai_embedding_adapter(provider) for provider in OPENAI_COMPAT_PROVIDERS}


def get_embedding_adapter(provider: str):
    if provider in ADAPTERS:
        return ADAPTERS[provider]
    if provider and (provider.startswith("openai-compatible-") or provider.startswith("custom-embedding-")):
        return openai_compat_node
    return None
