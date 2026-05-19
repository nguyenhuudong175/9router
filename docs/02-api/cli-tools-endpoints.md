# CLI Tools Endpoints

## Route family
- `/api/cli-tools/**` contains per-tool configuration writers/checkers.
- Examples: `claude-settings`, `codex-settings`, `cline-settings`, `openclaw-settings`, `cowork-settings`, `opencode-settings`.

## Access model
- High-risk host-mutating routes are additionally restricted to loopback requests by middleware local-only guards (`src/dashboardGuard.js`).

## UI coupling
- Dashboard pages under `src/app/(dashboard)/dashboard/cli-tools/**` consume these endpoints.
