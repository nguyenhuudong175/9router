# Development and Operations Guide

## Build and run

### Root application (Next.js)
- Dev: `npm run dev`
- Build: `npm run build`
- Start: `npm run start`

### Test suite
- Tests are in `/tests` and run with `npm test` from that directory.
- Current test script expects Vitest at `/tmp/node_modules/.bin/vitest`.

## Environment contract
Primary runtime variables (see `.env.example`):
- Security/auth: `JWT_SECRET`, `INITIAL_PASSWORD`, `API_KEY_SECRET`, `MACHINE_ID_SALT`.
- Storage/runtime: `DATA_DIR`, `PORT`, `NODE_ENV`, `HOSTNAME`.
- Cloud sync URLing: `BASE_URL`/`CLOUD_URL` and `NEXT_PUBLIC_BASE_URL`/`NEXT_PUBLIC_CLOUD_URL`.
- Logging: `ENABLE_REQUEST_LOGS`, `OBSERVABILITY_ENABLED`.
- API protection: `REQUIRE_API_KEY`.
- Proxy: `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY` (and lowercase variants).

## Deployment

### Docker image
- Multi-stage Docker build in `Dockerfile`.
- Runtime defaults: `PORT=20128`, `HOSTNAME=0.0.0.0`, `DATA_DIR=/app/data`.
- Standalone Next output + `open-sse` + MITM assets copied into runtime image.

### GitHub workflows
- `.github/workflows/docker-publish.yml`: builds/pushes multi-arch Docker images on version tags/manual dispatch.
- `.github/workflows/gitbook-pages.yml`: builds/deploys `gitbook/` static output to external pages repo.

## Runtime troubleshooting notes
- Build can fail in restricted networks if Google Fonts fetch is blocked during `next build`.
- Tests can fail if `/tmp/node_modules/.bin/vitest` has not been prepared.
- Provider-specific behavior depends on external OAuth/API availability and credentials.

## Recommended validation sequence
1. Install dependencies: `npm install`.
2. Build app: `npm run build`.
3. Prepare test runtime if needed: install Vitest under `/tmp/node_modules`.
4. Run tests: `cd tests && npm test`.
