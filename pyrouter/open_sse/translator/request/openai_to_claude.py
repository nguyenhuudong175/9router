import json

from pyrouter.open_sse.config.app_constants import CLAUDE_SYSTEM_PROMPT
from pyrouter.open_sse.translator.helpers.max_tokens_helper import adjust_max_tokens

CLAUDE_OAUTH_TOOL_PREFIX = ""


def openai_to_claude_request(model, body, stream):
    tool_name_map = {}
    result = {"model": model, "max_tokens": adjust_max_tokens(body), "stream": stream, "messages": []}

    if "temperature" in body:
        result["temperature"] = body["temperature"]

    system_parts = []
    messages = body.get("messages") or []
    if isinstance(messages, list):
        for msg in messages:
            if msg.get("role") == "system":
                system_parts.append(msg.get("content") if isinstance(msg.get("content"), str) else extract_text_content(msg.get("content")))

    response_format = body.get("response_format")
    if response_format:
        if response_format.get("type") == "json_schema" and (response_format.get("json_schema") or {}).get("schema"):
            schema_json = json.dumps(response_format["json_schema"]["schema"], indent=2)
            system_parts.append(
                "You must respond with valid JSON that strictly follows this JSON schema:\n"
                "```json\n"
                f"{schema_json}\n"
                "```\n"
                "Respond ONLY with the JSON object, no other text."
            )
        elif response_format.get("type") == "json_object":
            system_parts.append("You must respond with valid JSON. Respond ONLY with a JSON object, no other text.")

    claude_code_prompt = {"type": "text", "text": CLAUDE_SYSTEM_PROMPT}
    if system_parts:
        result["system"] = [
            claude_code_prompt,
            {"type": "text", "text": "\n".join([p for p in system_parts if p]), "cache_control": {"type": "ephemeral", "ttl": "1h"}},
        ]
    else:
        result["system"] = [claude_code_prompt]

    if body.get("tool_choice"):
        result["tool_choice"] = convert_openai_tool_choice(body.get("tool_choice"))

    if body.get("thinking"):
        thinking = body["thinking"]
        result["thinking"] = {
            "type": thinking.get("type") or "enabled",
            **({"budget_tokens": thinking.get("budget_tokens")} if thinking.get("budget_tokens") else {}),
            **({"max_tokens": thinking.get("max_tokens")} if thinking.get("max_tokens") else {}),
        }

    effort = body.get("reasoning_effort")
    if effort and not result.get("thinking"):
        effort_to_budget = {"none": 0, "low": 4096, "medium": 8192, "high": 16384, "xhigh": 32768}
        budget = effort_to_budget.get(str(effort).lower())
        if budget and budget > 0:
            result["thinking"] = {"type": "enabled", "budget_tokens": budget}

    if tool_name_map:
        result["_toolNameMap"] = tool_name_map

    return result


def convert_openai_tool_choice(choice):
    if not choice:
        return {"type": "auto"}
    if isinstance(choice, dict) and choice.get("type"):
        return choice
    if choice in ("auto", "none"):
        return {"type": "auto"}
    if choice == "required":
        return {"type": "any"}
    if isinstance(choice, dict) and choice.get("function"):
        return {"type": "tool", "name": choice["function"].get("name")}
    return {"type": "auto"}


def extract_text_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if part.get("type") == "text")
    return ""


def try_parse_json(value):
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value
