# SQLite Schema Summary

## Schema declaration
- `src/lib/db/schema.js` defines `TABLES` and `SCHEMA_VERSION`.

## Core tables
- `settings`, `providerConnections`, `providerNodes`, `proxyPools`, `apiKeys`, `combos`, `kv`.
- Usage tables: `usageHistory`, `usageDaily`.
- Diagnostics: `requestDetails`.

## Technical notes
- Many complex objects are stored as JSON text blobs (`data`, `tokens`, `meta`).
- Indexes are declared per table and auto-created during schema sync.
