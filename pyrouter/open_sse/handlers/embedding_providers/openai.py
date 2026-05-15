from ._base import bearer_auth

ENDPOINTS = {
    "openai": "https://api.openai.com/v1/embeddings",
    "openrouter": "https://openrouter.ai/api/v1/embeddings",
    "mistral": "https://api.mistral.ai/v1/embeddings",
    "voyage-ai": "https://api.voyageai.com/v1/embeddings",
    "fireworks": "https://api.fireworks.ai/inference/v1/embeddings",
    "together": "https://api.together.xyz/v1/embeddings",
    "nebius": "https://api.tokenfactory.nebius.com/v1/embeddings",
    "github": "https://models.github.ai/inference/embeddings",
    "nvidia": "https://integrate.api.nvidia.com/v1/embeddings",
    "jina-ai": "https://api.jina.ai/v1/embeddings",
}


class OpenAIEmbeddingAdapter:
    def __init__(self, provider_id: str):
        self.provider_id = provider_id

    def build_url(self, model, creds, ctx=None):
        return ENDPOINTS[self.provider_id]

    def build_headers(self, creds, ctx=None):
        headers = {"Content-Type": "application/json", **bearer_auth(creds)}
        if self.provider_id == "openrouter":
            headers["HTTP-Referer"] = "https://endpoint-proxy.local"
            headers["X-Title"] = "Endpoint Proxy"
        return headers

    def build_body(self, model, payload):
        body = {"model": model, "input": payload.get("input")}
        encoding = payload.get("encoding_format")
        if encoding:
            body["encoding_format"] = encoding
        dimensions = payload.get("dimensions")
        if dimensions not in (None, ""):
            try:
                dim = int(dimensions)
                if dim > 0:
                    body["dimensions"] = dim
            except Exception:
                pass
        return body

    def normalize(self, response_body, model=None):
        return response_body


def create_openai_embedding_adapter(provider_id: str):
    return OpenAIEmbeddingAdapter(provider_id)
