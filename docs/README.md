# 9Router Repository Analysis Docs

This documentation set is implementation-grounded and generated from the code under `src/`, `open-sse/`, `cli/`, `tests/`, and root runtime/config files.

## Structure
- `00-overview`: repository map, runtime matrix, dependency/build baseline.
- `01-runtime`: request execution, translation, streaming, fallback, RTK.
- `02-api`: App Router API surfaces by domain.
- `03-data`: SQLite schema, migrations, repo APIs, shims.
- `04-security`: auth/session/API-key/middleware boundaries.
- `05-ui`: dashboard composition and state stores.
- `06-integrations`: providers, OAuth, cloud sync, tunnels/MITM.
- `07-operations`: Docker/CLI/env/rebuild/troubleshooting.
- `08-quality`: testing baseline and risk gaps.
- `09-reference`: file index and glossary.

## Baseline Source Anchors
- Next.js routing and rewrites: `next.config.mjs`
- API routes: `src/app/api/**/route.js`
- Core execution: `src/sse/**`, `open-sse/**`
- Persistence: `src/lib/db/**`
- Middleware and auth: `src/dashboardGuard.js`, `src/lib/auth/**`
