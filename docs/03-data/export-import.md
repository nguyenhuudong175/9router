# Export/Import Behavior

## Export
- `exportDb()` reads current table data and reconstructs logical JSON shape (connections, settings, aliases, pricing, etc.).

## Import
- `importDb(payload)` wipes mutable tables (except metadata) and re-inserts normalized records in one transaction.

## Risk note
- Import is full-state replacement for config tables; operational consumers should treat it as authoritative restore.
