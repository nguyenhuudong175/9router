# Docker Deployment

## Build and runtime image
- Multi-stage Dockerfile builds Next standalone bundle, then copies static assets and required runtime modules.
- Runtime defaults: `PORT=20128`, `HOSTNAME=0.0.0.0`, `DATA_DIR=/app/data`.

## Persistence
- Recommended bind mount: `$HOME/.9router:/app/data`.
- Main DB in container: `/app/data/db/data.sqlite`.

## Notable packaging detail
- Docker image explicitly copies `open-sse/`, `src/mitm`, `node-forge`, and `next` to avoid tracing omissions.
