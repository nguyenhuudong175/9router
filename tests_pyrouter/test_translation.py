import unittest

from pyrouter.translation.translator import Translator


class TranslationTests(unittest.TestCase):
    def test_openai_to_claude(self):
        body = {"messages": [{"role": "user", "content": "hello"}]}
        out = Translator.translate_request("openai", "claude", body)
        self.assertEqual(out["messages"][0]["content"][0]["type"], "text")
        self.assertEqual(out["anthropic_version"], "2023-06-01")

    def test_claude_to_openai(self):
        body = {"anthropic_version": "2023-06-01", "messages": [{"role": "user", "content": [{"type": "text", "text": "hello"}]}]}
        out = Translator.translate_request("claude", "openai", body)
        self.assertEqual(out["messages"][0]["content"], "hello")

    def test_response_translation_claude_to_openai(self):
        body = {"id": "m1", "model": "claude-4", "content": [{"type": "text", "text": "ok"}], "usage": {"input_tokens": 10, "output_tokens": 5}}
        out = Translator.translate_response("claude", "openai", body)
        self.assertEqual(out["choices"][0]["message"]["content"], "ok")
        self.assertEqual(out["usage"]["total_tokens"], 15)


if __name__ == "__main__":
    unittest.main()

