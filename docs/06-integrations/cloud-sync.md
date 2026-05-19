# Cloud Sync Integration

## Scheduler
- `CloudSyncScheduler` (`src/shared/services/cloudSyncScheduler.js`) triggers periodic sync calls.
- First sync delayed 30s, then recurring every configured interval (default 15 min).

## Control checks
- Sync runs only when `isCloudEnabled()` returns true from settings storage.
- Scheduler posts to internal API endpoint `${BASE_URL}/api/sync/cloud` with machine ID.

## Initialization
- Root layout imports `@/lib/initCloudSync`, which ensures app bootstrap singleton and auto-init outside build phase.

## Caveat
- Route path `/api/sync/cloud` is referenced by scheduler but no matching file was found under `src/app/api/sync/**` during this analysis pass.
