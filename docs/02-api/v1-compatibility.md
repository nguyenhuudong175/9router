# V1 Compatibility APIs

## Routing
- External `/v1/*` is rewritten to `/api/v1/*` (`next.config.mjs`).
- `/codex/*` is rewritten to `/api/v1/responses`.

## Main handlers
- Chat: `src/app/api/v1/chat/completions/route.js`.
- Messages: `src/app/api/v1/messages/route.js`.
- Responses: `src/app/api/v1/responses/route.js` and `/compact`.
- Embeddings: `src/app/api/v1/embeddings/route.js`.
- Audio: `/audio/speech`, `/audio/transcriptions`, `/audio/voices`.
- Images: `/images/generations`.

## Behavior
- Compatibility routes mostly delegate into `src/sse/handlers/*` and `open-sse/handlers/*`.
