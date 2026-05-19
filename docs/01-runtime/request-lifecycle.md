# Request Lifecycle

## Entry points
- `/api/v1/chat/completions` delegates to `handleChat` (`src/app/api/v1/chat/completions/route.js`).
- `handleChat` is implemented in `src/sse/handlers/chat.js`.

## Main flow
1. Parse JSON body and log endpoint/model metadata.
2. Resolve auth policy (`requireApiKey`) via settings.
3. Resolve model alias/combo via `getModelInfo`/`getComboModels`.
4. Select provider credentials with fallback exclusions.
5. Call `open-sse/handlers/chatCore.js` for translation + execution.
6. On provider/account errors, mark account unavailable and retry next account.

## Completion semantics
- Returns direct provider response on success.
- Returns unavailable/error responses with retry hints for throttling paths.
