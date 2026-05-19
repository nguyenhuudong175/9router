# Data Model and State Management

## Storage root
- Storage location is derived from `DATA_DIR` (`src/lib/dataDir.js`).
- Default fallback is platform-specific user directory (`~/.9router` on non-Windows).

## Primary DB implementation
- SQLite database file: `${DATA_DIR}/db/data.sqlite`.
- Backups: `${DATA_DIR}/db/backups`.
- Adapter fallback chain in `src/lib/db/driver.js`:
  - Bun runtime: `bun:sqlite` then `sql.js`.
  - Node runtime: `better-sqlite3` then `node:sqlite` (Node >=22.5) then `sql.js`.

## Schema and migration
- Schema version: `SCHEMA_VERSION = 1`.
- Initial migration: `src/lib/db/migrations/001-initial.js`.
- Declarative table/index definitions in `src/lib/db/schema.js`.

## Core tables (from schema)
- `_meta`: migration metadata and app metadata.
- `settings`: singleton settings payload.
- `providerConnections`: provider account credentials/config.
- `providerNodes`: custom compatible upstream endpoints.
- `proxyPools`: proxy pool definitions/test state.
- `apiKeys`: generated local gateway API keys.
- `combos`: named model fallback groups.
- `kv`: scoped key-value records (aliases, pricing, custom models, etc.).
- `usageHistory`, `usageDaily`: token/cost usage tracking.
- `requestDetails`: detailed per-request diagnostic snapshots.

## Repository pattern
- DB access is modularized via repos in `src/lib/db/repos/**`.
- `src/lib/db/index.js` is the public facade for route/runtime code.
- Legacy modules (`src/lib/localDb.js`, `src/lib/usageDb.js`) are compatibility shims that re-export DB facade methods.

## Import/export behavior
- Full logical DB export/import is implemented in `src/lib/db/index.js`.
- Export normalizes JSON payloads from row + data column patterns.
- Import wipes selected tables/scopes then restores normalized payloads transactionally.

## Operational data considerations
- DB contains provider secrets/tokens and API keys.
- Request/usage records may include sensitive metadata and should be handled as protected local state.
