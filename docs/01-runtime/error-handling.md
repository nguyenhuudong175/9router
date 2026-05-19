# Runtime Error Handling

## Upstream errors
- `parseUpstreamError` and `formatProviderError` normalize provider failures (`open-sse/utils/error.js`).
- Error responses preserve status code and optional reset hints.

## Account fallback
- Failed account is marked unavailable and cooldowned via `markAccountUnavailable` (`src/sse/services/auth.js`, `open-sse/services/accountFallback.js`).
- Handler retries alternate accounts until exhausted.

## Abort/disconnect
- Abort errors map to 499 semantics and stop pending tracking.
