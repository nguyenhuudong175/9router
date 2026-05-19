# Troubleshooting Guide

## Build fails with `next: not found`
- Install app dependencies in repository root (`npm install`) before `npm run build`.

## Tests fail with missing vitest binary
- Tests package expects binary in `/tmp/node_modules/.bin/vitest`; install there or adjust environment to match `tests/package.json`.

## No provider responses / frequent fallback
- Inspect usage/request logs endpoints and provider test endpoints.
- Verify credentials in `/api/providers/[id]/test` and rate-limit cooldown status.

## Dashboard auth loops
- Check `requireLogin` setting and JWT secret persistence in `${DATA_DIR}/jwt-secret`.
