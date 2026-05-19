# Streaming and Non-Streaming Handling

## Decision logic
- `chatCore` computes stream mode from request body, source format, provider requirements, and `Accept` header.
- `openai`, `codex`, and `commandcode` can force streaming upstream.

## Handler branches
- Forced SSE->JSON adaptation: `chatCore/sseToJsonHandler.js`.
- Non-stream path: `chatCore/nonStreamingHandler.js`.
- Stream path: `chatCore/streamingHandler.js` with disconnect-aware controller.

## Usage and request detail capture
- Pending state, log lines, and request detail snapshots are persisted through `usageDb` APIs.
