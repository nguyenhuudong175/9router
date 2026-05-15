from dataclasses import dataclass
import json


@dataclass
class HttpResponse:
    body: str
    status: int
    headers: dict

    def json(self):
        return json.loads(self.body)


DEFAULT_ERROR_MESSAGES = {
    400: "Bad request",
    401: "Unauthorized",
    403: "Forbidden",
    429: "Rate limited",
    500: "Server error",
    502: "Bad gateway",
}


def build_error_body(status_code: int, message: str | None):
    return {
        "error": {
            "message": message or DEFAULT_ERROR_MESSAGES.get(status_code, "An error occurred"),
            "type": "server_error" if status_code >= 500 else "invalid_request_error",
            "code": "internal_server_error" if status_code >= 500 else "",
        }
    }


def error_response(status_code: int, message: str):
    return HttpResponse(
        body=json.dumps(build_error_body(status_code, message)),
        status=status_code,
        headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
    )


async def parse_upstream_error(response, executor=None):
    try:
        body_text = await response.text()
    except Exception:
        body_text = ""

    if executor and callable(getattr(executor, "parse_error", None)):
        try:
            parsed = executor.parse_error(response, body_text)
            if isinstance(parsed, dict):
                msg = parsed.get("message") or DEFAULT_ERROR_MESSAGES.get(response.status) or f"Upstream error: {response.status}"
                return {"statusCode": parsed.get("status", response.status), "message": msg, "resetsAtMs": parsed.get("resetsAtMs")}
        except Exception:
            pass

    try:
        body = json.loads(body_text) if body_text else {}
        message = body.get("error", {}).get("message") or body.get("message") or body.get("error") or body_text
    except Exception:
        message = body_text

    if not isinstance(message, str):
        message = json.dumps(message)

    return {"statusCode": response.status, "message": message or DEFAULT_ERROR_MESSAGES.get(response.status) or f"Upstream error: {response.status}"}


def create_error_result(status_code: int, message: str, resets_at_ms=None):
    return {
        "success": False,
        "status": status_code,
        "error": message,
        "resetsAtMs": resets_at_ms,
        "response": error_response(status_code, message),
    }


def format_provider_error(error: Exception, provider: str, model: str, status_code):
    code = status_code or getattr(error, "code", None) or "FETCH_FAILED"
    message = str(error) or "Unknown error"
    return f"[{code}]: {message}"
