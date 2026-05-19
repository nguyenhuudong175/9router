# 9Router Architecture

## System context
9Router runs as a single Next.js process that hosts both dashboard APIs and OpenAI-compatible gateway endpoints. It routes requests to upstream AI providers through a translation + executor pipeline and stores configuration/usage in local SQLite data files.

## Core architectural layers

### 1) API ingress (Next.js routes)
- Compatibility/gateway endpoints: `src/app/api/v1/**`, `src/app/api/v1beta/**`.
- Dashboard/management endpoints: `src/app/api/**` (providers, settings, auth, usage, sync, proxy pools, etc.).
- URL rewrite mapping in `next.config.mjs` maps `/v1/*` to `/api/v1/*`.

### 2) Request orchestration layer
- Entry handler: `src/sse/handlers/chat.js`.
- Responsibilities:
  - request parsing + format hints,
  - API key enforcement (`requireApiKey`),
  - model/combo resolution,
  - account selection and fallback loop,
  - token pre-refresh hooks,
  - delegation to core execution.

### 3) Core execution/translation layer
- Main core: `open-sse/handlers/chatCore.js`.
- Responsibilities:
  - source-format detection,
  - target-format selection by provider/model,
  - request translation,
  - native passthrough optimization,
  - request shaping (RTK compression, caveman prompt injection, tool dedupe),
  - executor dispatch + upstream call,
  - 401/403 refresh-and-retry path,
  - streaming/non-streaming response normalization,
  - request/usage logging.

### 4) Provider execution layer
- Executors under `open-sse/executors/*`.
- `open-sse/executors/index.js` resolves executor by provider.
- Specialized executors exist for providers that require custom auth/transport/protocol behavior.

### 5) Persistence layer
- Public DB API: `src/lib/db/index.js`.
- Runtime adapter bootstrap: `src/lib/db/driver.js`.
- Data paths: `src/lib/db/paths.js` (`${DATA_DIR}/db/data.sqlite`, backups under `${DATA_DIR}/db/backups`).
- Schema in `src/lib/db/schema.js`; initial migration in `src/lib/db/migrations/001-initial.js`.

## Important runtime flows

### Chat flow (`/v1/chat/completions`)
1. Route `src/app/api/v1/chat/completions/route.js` initializes translator and calls `handleChat`.
2. `handleChat` resolves model/provider/combo and obtains credentials.
3. `handleChatCore` translates and executes upstream call.
4. Response is streamed or normalized to JSON for client compatibility.
5. Usage + request details are persisted.

### Fallback behavior
- Account fallback is handled when errors indicate temporary/provider-specific unavailability.
- Combo fallback can switch to the next model in configured combo sequence.
- Retry-after and cooldown semantics are tracked and surfaced for unavailable states.

### Data-path behavior
- `DATA_DIR` controls storage root (`src/lib/dataDir.js`), with writable fallback to `~/.9router`.
- Legacy JSON files are tracked in `LEGACY_FILES` metadata for migration/back-compat paths.

## Security-sensitive boundaries
- Dashboard auth and cookie/session flow live under `src/app/api/auth/*` and `src/dashboardGuard.js`.
- API keys are generated/validated via DB-backed key records.
- Provider credentials/tokens are persisted in DB and must be protected at filesystem/runtime level.
- Optional outbound proxy settings can affect all upstream provider traffic.

## Extensibility model
- Add provider support by extending provider constants + model registry + executor/translator mappings.
- Add API capability by implementing route handler + core handler + DB repository (when persistence needed).
- DB schema evolution uses versioned migrations plus declarative table/index synchronization.
