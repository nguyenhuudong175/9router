import json
import pytest

import pyrouter.open_sse.handlers.embeddings_core as target


class FakeResponse:
    def __init__(self, body, status=200, ok=True):
        self._body = body
        self.status = status
        self.ok = ok

    async def json(self):
        if isinstance(self._body, Exception):
            raise self._body
        return self._body

    async def text(self):
        if isinstance(self._body, dict):
            return json.dumps(self._body)
        return str(self._body)


class Executor:
    no_auth = False

    def __init__(self, refreshed=None):
        self._refreshed = refreshed or {}

    async def refresh_credentials(self, credentials, log):
        return self._refreshed


@pytest.mark.asyncio
async def test_missing_input_returns_400():
    result = await target.handle_embeddings_core(
        body={"model": "x"},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "k"},
        fetch=None,
    )
    assert result["success"] is False
    assert result["status"] == 400


@pytest.mark.asyncio
async def test_invalid_input_type_returns_400():
    result = await target.handle_embeddings_core(
        body={"model": "x", "input": 123},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "k"},
        fetch=None,
    )
    assert result["success"] is False
    assert result["status"] == 400


@pytest.mark.asyncio
async def test_unsupported_provider_returns_400():
    result = await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "antigravity", "model": "x"},
        credentials={"apiKey": "k"},
        fetch=None,
    )
    assert result["success"] is False
    assert result["status"] == 400


@pytest.mark.asyncio
async def test_openai_url_and_default_encoding():
    calls = []

    async def fake_fetch(url, init):
        calls.append((url, init))
        return FakeResponse({"object": "list", "data": [], "usage": {}}, status=200, ok=True)

    result = await target.handle_embeddings_core(
        body={"model": "text-embedding-ada-002", "input": "Hello world"},
        model_info={"provider": "openai", "model": "text-embedding-ada-002"},
        credentials={"apiKey": "sk-test"},
        fetch=fake_fetch,
    )

    assert result["success"] is True
    assert calls[0][0] == "https://api.openai.com/v1/embeddings"
    sent = json.loads(calls[0][1]["body"])
    assert sent["encoding_format"] == "float"


@pytest.mark.asyncio
async def test_openrouter_headers_include_referer_title():
    calls = []

    async def fake_fetch(url, init):
        calls.append((url, init))
        return FakeResponse({"object": "list", "data": [], "usage": {}}, status=200, ok=True)

    await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "openrouter", "model": "x"},
        credentials={"apiKey": "sk-or-test"},
        fetch=fake_fetch,
    )

    headers = calls[0][1]["headers"]
    assert headers["HTTP-Referer"] == "https://endpoint-proxy.local"
    assert headers["X-Title"] == "Endpoint Proxy"


@pytest.mark.asyncio
async def test_openai_compatible_base_url_and_trailing_slash():
    calls = []

    async def fake_fetch(url, init):
        calls.append((url, init))
        return FakeResponse({"object": "list", "data": [], "usage": {}}, status=200, ok=True)

    await target.handle_embeddings_core(
        body={"model": "embed-v1", "input": "hello"},
        model_info={"provider": "openai-compatible-custom", "model": "embed-v1"},
        credentials={"apiKey": "sk", "providerSpecificData": {"baseUrl": "https://myhost.ai/v1/"}},
        fetch=fake_fetch,
    )

    assert calls[0][0] == "https://myhost.ai/v1/embeddings"


@pytest.mark.asyncio
async def test_network_error_returns_502():
    async def fake_fetch(url, init):
        raise RuntimeError("fetch failed")

    result = await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "sk"},
        fetch=fake_fetch,
    )

    assert result["success"] is False
    assert result["status"] == 502


@pytest.mark.asyncio
async def test_provider_error_429_returns_error_result():
    async def fake_fetch(url, init):
        return FakeResponse({"error": {"message": "Too many requests"}}, status=429, ok=False)

    result = await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "sk"},
        fetch=fake_fetch,
    )

    assert result["success"] is False
    assert result["status"] == 429


@pytest.mark.asyncio
async def test_invalid_json_from_provider_returns_502():
    async def fake_fetch(url, init):
        return FakeResponse(ValueError("invalid"), status=200, ok=True)

    result = await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "sk"},
        fetch=fake_fetch,
    )

    assert result["success"] is False
    assert result["status"] == 502


@pytest.mark.asyncio
async def test_token_refresh_retries_on_401(monkeypatch):
    calls = []
    responses = [
        FakeResponse({"error": {"message": "Unauthorized"}}, status=401, ok=False),
        FakeResponse({"object": "list", "data": [], "usage": {}}, status=200, ok=True),
    ]

    async def fake_fetch(url, init):
        calls.append((url, init))
        return responses.pop(0)

    monkeypatch.setattr(target, "get_executor", lambda provider: Executor(refreshed={"accessToken": "new-token"}))

    refreshed = {}

    async def on_ref(new_credentials):
        refreshed.update(new_credentials)

    result = await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "old-token"},
        fetch=fake_fetch,
        on_credentials_refreshed=on_ref,
    )

    assert result["success"] is True
    assert len(calls) == 2
    assert refreshed.get("accessToken") == "new-token"


@pytest.mark.asyncio
async def test_success_response_includes_json_and_cors():
    async def fake_fetch(url, init):
        return FakeResponse({"object": "list", "data": [{"embedding": [0.1]}], "usage": {}}, status=200, ok=True)

    called = {"ok": False}

    async def on_success():
        called["ok"] = True

    result = await target.handle_embeddings_core(
        body={"model": "x", "input": "hello"},
        model_info={"provider": "openai", "model": "x"},
        credentials={"apiKey": "sk"},
        fetch=fake_fetch,
        on_request_success=on_success,
    )

    assert result["success"] is True
    assert result["response"].headers["Content-Type"] == "application/json"
    assert result["response"].headers["Access-Control-Allow-Origin"] == "*"
    assert called["ok"] is True
