import json

from pyrouter.open_sse.config.runtime_config import HTTP_STATUS
from pyrouter.open_sse.executors.index import get_executor
from pyrouter.open_sse.handlers.embedding_providers.index import get_embedding_adapter
from pyrouter.open_sse.services.token_refresh import refresh_with_retry
from pyrouter.open_sse.utils.error import create_error_result, format_provider_error, parse_upstream_error, HttpResponse


async def handle_embeddings_core(
    *,
    body,
    model_info,
    credentials,
    log=None,
    on_credentials_refreshed=None,
    on_request_success=None,
    fetch=None,
):
    provider = model_info.get("provider")
    model = model_info.get("model")

    input_value = body.get("input")
    if not input_value:
        return create_error_result(HTTP_STATUS["BAD_REQUEST"], "Missing required field: input")
    if not isinstance(input_value, str) and not isinstance(input_value, list):
        return create_error_result(HTTP_STATUS["BAD_REQUEST"], "input must be a string or array of strings")

    adapter = get_embedding_adapter(provider)
    if not adapter:
        return create_error_result(HTTP_STATUS["BAD_REQUEST"], f"Provider '{provider}' does not support embeddings.")

    ctx = {"input": input_value}
    url = adapter.build_url(model, credentials, ctx)
    headers = adapter.build_headers(credentials, ctx)
    request_body = adapter.build_body(
        model,
        {
            "input": input_value,
            "encoding_format": body.get("encoding_format") or "float",
            "dimensions": body.get("dimensions"),
        },
    )

    try:
        provider_response = await fetch(url, {"method": "POST", "headers": headers, "body": json.dumps(request_body)})
    except Exception as error:
        err_msg = format_provider_error(error, provider, model, HTTP_STATUS["BAD_GATEWAY"])
        return create_error_result(HTTP_STATUS["BAD_GATEWAY"], err_msg)

    executor = get_executor(provider)
    if executor and not getattr(executor, "no_auth", False) and provider_response.status in (HTTP_STATUS["UNAUTHORIZED"], HTTP_STATUS["FORBIDDEN"]):
        new_credentials = await refresh_with_retry(lambda: executor.refresh_credentials(credentials, log), 3, log)
        if new_credentials and (new_credentials.get("accessToken") or new_credentials.get("apiKey")):
            credentials.update(new_credentials)
            if on_credentials_refreshed:
                await on_credentials_refreshed(new_credentials)
            try:
                retry_headers = adapter.build_headers(credentials, ctx)
                retry_url = adapter.build_url(model, credentials, ctx)
                provider_response = await fetch(retry_url, {"method": "POST", "headers": retry_headers, "body": json.dumps(request_body)})
            except Exception:
                pass

    if not provider_response.ok:
        parsed = await parse_upstream_error(provider_response)
        err_msg = format_provider_error(Exception(parsed["message"]), provider, model, parsed["statusCode"])
        return create_error_result(parsed["statusCode"], err_msg)

    try:
        response_body = await provider_response.json()
    except Exception:
        return create_error_result(HTTP_STATUS["BAD_GATEWAY"], f"Invalid JSON response from {provider}")

    if on_request_success:
        await on_request_success()

    normalized = adapter.normalize(response_body, model)
    return {
        "success": True,
        "response": HttpResponse(
            body=json.dumps(normalized),
            status=200,
            headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        ),
    }
