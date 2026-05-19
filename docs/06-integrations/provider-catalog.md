# Provider Catalog (Code-Defined)

## Source of truth
- Provider metadata is centralized in `open-sse/config/providers.js`.

## Major provider groups in code
- OAuth/credential-refresh oriented: claude, codex, github, gemini-cli, cursor, kiro, qwen, iflow, qoder, antigravity.
- API-key style: openai, openrouter, anthropic, deepseek, minimax, kimi, glm, nvidia, etc.
- Web/local adapters: grok-web, perplexity-web, ollama-local, opencode.

## Routing format coupling
- Each provider declares target format (`openai`, `claude`, `gemini`, `cursor`, `commandcode`, etc.) consumed by translation and executor layers.
