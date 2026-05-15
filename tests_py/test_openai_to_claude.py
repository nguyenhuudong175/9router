from pyrouter.open_sse.translator.request.openai_to_claude import openai_to_claude_request


def _system_text(result):
    return "\n".join(s["text"] for s in result.get("system", []) if s.get("type") == "text")


def test_injects_json_schema_instructions():
    body = {
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "math_response",
                "schema": {
                    "type": "object",
                    "properties": {"answer": {"type": "number"}, "explanation": {"type": "string"}},
                    "required": ["answer", "explanation"],
                },
            },
        },
    }
    result = openai_to_claude_request("claude-sonnet-4.5", body, False)
    system_text = _system_text(result)
    assert "You must respond with valid JSON" in system_text
    assert '"answer"' in system_text
    assert '"explanation"' in system_text
    assert "Respond ONLY with the JSON object" in system_text


def test_injects_json_object_instructions():
    body = {
        "messages": [{"role": "user", "content": "Give me a JSON object"}],
        "response_format": {"type": "json_object"},
    }
    result = openai_to_claude_request("claude-sonnet-4.5", body, False)
    system_text = _system_text(result)
    assert "You must respond with valid JSON" in system_text
    assert "Respond ONLY with a JSON object" in system_text


def test_no_response_format_does_not_add_json_instructions():
    body = {"messages": [{"role": "user", "content": "Hello"}]}
    result = openai_to_claude_request("claude-sonnet-4.5", body, False)
    assert "You must respond with valid JSON" not in _system_text(result)


def test_preserves_existing_system_message():
    body = {
        "messages": [
            {"role": "system", "content": "You are a helpful math tutor."},
            {"role": "user", "content": "What is 2+2?"},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": {"type": "object", "properties": {"result": {"type": "number"}}}},
        },
    }
    result = openai_to_claude_request("claude-sonnet-4.5", body, False)
    system_text = _system_text(result)
    assert "You are a helpful math tutor" in system_text
    assert "You must respond with valid JSON" in system_text
