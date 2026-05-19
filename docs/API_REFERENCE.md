# API Surface Reference (Repository-Level)

This document maps the major API route groups implemented in `src/app/api/**`.

## Compatibility/Gateway APIs

### `/api/v1/*` (rewritten from `/v1/*`)
- Chat: `/v1/chat/completions`, `/v1/messages`, `/v1/responses`.
- Models: `/v1/models`, `/v1/models/info`, `/v1/models/[kind]`.
- Media: `/v1/images/generations`, `/v1/audio/speech`, `/v1/audio/transcriptions`, `/v1/audio/voices`.
- Embeddings: `/v1/embeddings`.
- Utility: `/v1/messages/count_tokens`, `/v1/search`, `/v1/web/fetch`, `/v1/api/chat`.

### `/api/v1beta/*`
- Beta models endpoint pass-through/compat wrappers.

## Dashboard and Management APIs

### Auth and session
- `/api/auth/login`, `/api/auth/logout`, `/api/auth/status`.
- OIDC flow under `/api/auth/oidc/*`.

### Providers and credentials
- `/api/providers/*` (CRUD, validation, tests, model discovery).
- `/api/provider-nodes/*` for compatible-node definitions.
- `/api/oauth/*` for provider OAuth/device flows and imports.

### Model governance
- `/api/models/*` (availability/custom/disabled/alias/test).
- `/api/combos/*` (fallback groups).
- `/api/pricing` (pricing overrides used for usage/cost views).

### API keys and settings
- `/api/keys/*`.
- `/api/settings/*` including require-login, proxy test, and DB actions.

### Usage and observability
- `/api/usage/*` (history, stats, chart, logs, streaming, request details).

### Sync and cloud helpers
- `/api/sync/*` and `/api/cloud/*` for cloud sync/auth/model alias helpers.

### CLI-tool integrations
- `/api/cli-tools/*` writes/validates local config integrations for external developer tools.

### Tunnel/version/health/ops
- `/api/tunnel/*`, `/api/version/*`, `/api/health`, `/api/shutdown`, `/api/init`, `/api/tags`.

## Internal API composition pattern
- Route handlers are thin controllers.
- Core logic is delegated to shared handlers/services in `src/sse/**` and `open-sse/**`.
- DB write/read logic is isolated in `src/lib/db/repos/**`.

## Notable protocol behaviors
- CORS OPTIONS handlers are implemented for compatibility endpoints.
- Streaming responses use SSE and may be converted to JSON for clients that require non-streaming.
- Request format detection/translation allows multiple client ecosystems to target one endpoint.
