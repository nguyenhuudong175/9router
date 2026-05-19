# Repository Map

## Top-level modules
- `src/app`: Next.js App Router pages and API routes.
- `src/sse`: request entry handlers and model/auth orchestration.
- `open-sse`: provider executors, translation, RTK filters, stream handling.
- `src/lib/db`: SQLite adapters, schema, migrations, repositories.
- `src/shared`: dashboard components, stores, constants, utilities.
- `cli`: published `9router` CLI package and build hooks.
- `tests`: Vitest suite for embeddings paths.

## Entry behavior
- Root layout imports `@/lib/initCloudSync` and outbound proxy bootstrap (`src/app/layout.js`).
- Middleware proxy guard is exported through `src/proxy.js` and implemented in `src/dashboardGuard.js`.

## Routing bridge
- `/v1/*` and `/codex/*` are rewritten to App Router API routes (`next.config.mjs`).
