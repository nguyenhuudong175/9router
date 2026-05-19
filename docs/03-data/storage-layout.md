# Storage Layout

## Data directory resolution
- `DATA_DIR` controls root path (`src/lib/dataDir.js`), with fallback `~/.9router` (or `%APPDATA%/9router` on Windows).

## Primary files
- Main DB: `${DATA_DIR}/db/data.sqlite` (`src/lib/db/paths.js`).
- Backups: `${DATA_DIR}/db/backups`.
- Legacy import candidates: `${DATA_DIR}/db.json`, `usage.json`, `disabledModels.json`, `request-details.json`.

## Compatibility behavior
- Legacy JSON files are imported one-time into SQLite on fresh DB migrations (`src/lib/db/migrate.js`).
