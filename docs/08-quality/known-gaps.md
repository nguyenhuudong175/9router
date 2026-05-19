# Known Documentation and Validation Gaps

## Code-level gaps observed
- Existing legacy `docs/ARCHITECTURE.md` includes stale storage references (`db.json`, `usage.json`) while active paths are SQLite-first.
- Scheduler references `/api/sync/cloud`, but route file was not found during this pass.

## Validation gaps in environment
- Build/test commands failed due missing dependencies in this execution environment.
- No end-to-end runtime verification was possible without provisioning those dependencies.
