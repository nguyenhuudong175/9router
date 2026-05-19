# Environment Variables (Observed)

## Core server
- `PORT`, `HOSTNAME`, `NODE_ENV`, `NEXT_DIST_DIR`, `NEXT_TRACING_ROOT_MODE`.

## Data/security
- `DATA_DIR`, `JWT_SECRET`, `AUTH_COOKIE_SECURE`, `API_KEY_SECRET`, `MACHINE_ID_SALT`.

## Feature/control flags
- `ENABLE_REQUEST_LOGS`, `ENABLE_TRANSLATOR`, outbound proxy vars (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY`).

## URL plumbing
- `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_CLOUD_URL`, and `BASE_URL` used by internal sync scheduler.
