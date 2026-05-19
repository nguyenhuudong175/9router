# Migration Strategy

## Runner
- `runMigrationOnce(adapter)` in `src/lib/db/migrate.js` orchestrates startup migration.

## Stages
1. Ensure `_meta` exists.
2. Apply versioned migrations from `src/lib/db/migrations/*`.
3. Additive schema sync for missing columns/indexes.
4. One-time legacy JSON import on fresh DB with marker file.
5. Backup on app version/schema upgrades.

## Safety
- Uses transaction boundaries and backup snapshots before destructive risk points.
