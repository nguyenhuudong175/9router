# Runtime Matrix

## Primary runtime
- Framework: Next.js standalone output (`next.config.mjs`, `output: "standalone"`).
- Node runtime expected for app server and CLI launcher (`package.json`, `cli/package.json`).

## Persistence runtime
- Data root resolved from `DATA_DIR` with fallback to home profile (`src/lib/dataDir.js`).
- Main DB path: `${DATA_DIR}/db/data.sqlite` (`src/lib/db/paths.js`).

## Optional runtimes
- Tunnel services: cloudflared/tailscale controls (`src/lib/tunnel/**`, `src/shared/services/initializeApp.js`).
- MITM subsystem with standalone process integration (`src/mitm/**`, initialize hooks in `initializeApp.js`).
