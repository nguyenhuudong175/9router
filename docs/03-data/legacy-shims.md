# Legacy Shim Modules

## Current role
- `src/lib/localDb.js` and `src/lib/usageDb.js` are compatibility shims exporting functions from `src/lib/db/index.js`.

## Why it matters
- Existing route and handler imports can remain stable while internals migrated from JSON storage to SQLite repositories.

## Migration implication
- New feature work should target `src/lib/db/**` as source of truth.
