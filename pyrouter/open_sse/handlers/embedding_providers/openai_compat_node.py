from .openai import create_openai_embedding_adapter

_base = create_openai_embedding_adapter("openai")


class OpenAICompatNodeAdapter:
    def build_url(self, model, creds, ctx=None):
        provider_data = creds.get("providerSpecificData") or {}
        raw_base_url = provider_data.get("baseUrl") or "https://api.openai.com/v1"
        base_url = raw_base_url.rstrip("/")
        if base_url.endswith("/embeddings"):
            base_url = base_url[: -len("/embeddings")]
        return f"{base_url}/embeddings"

    def build_headers(self, creds, ctx=None):
        return _base.build_headers(creds, ctx)

    def build_body(self, model, payload):
        return _base.build_body(model, payload)

    def normalize(self, response_body, model=None):
        return _base.normalize(response_body, model)


openai_compat_node = OpenAICompatNodeAdapter()
