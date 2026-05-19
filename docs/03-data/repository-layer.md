# Repository Layer

## Public DB barrel
- `src/lib/db/index.js` re-exports domain repository APIs.

## Repository domains
- Settings, connections, provider nodes, proxy pools, API keys, combos.
- Aliases/custom/mitm alias kv records.
- Pricing, disabled models, usage, request details.

## Adapter abstraction
- `src/lib/db/driver.js` selects concrete adapter implementations (`betterSqlite`, `sql.js`, `node:sqlite`, bun variant).
