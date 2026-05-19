# Executor Selection

## Dispatch
- `getExecutor(provider)` in `open-sse/executors/index.js` returns specialized executor if mapped.
- Unknown providers use cached `DefaultExecutor(provider)` instances.

## Specialized executors present
- `antigravity`, `azure`, `gemini-cli`, `github`, `iflow`, `qoder`, `kiro`, `codex`, `cursor`, `vertex`, `qwen`, `opencode`, `opencode-go`, `grok-web`, `perplexity-web`, `ollama-local`, `commandcode`.

## Auth retry coupling
- `chatCore` performs token refresh/retry for 401/403 when executor supports auth refresh.
