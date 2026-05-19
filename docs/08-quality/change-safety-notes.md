# Change Safety Notes

## High-impact areas
- `open-sse/handlers/chatCore.js`: central execution path, affects all chat traffic.
- `src/dashboardGuard.js`: auth and access control for nearly all app APIs.
- `src/lib/db/migrate.js`: startup migration and backup/import behavior.

## Safer extension patterns
- Add new provider behavior through executor map + provider config.
- Keep route-level logic thin; delegate to services/repos.
- Preserve shim exports (`localDb`, `usageDb`) to avoid broad import churn.
