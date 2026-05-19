# CLI Tools UI

## Location
- `src/app/(dashboard)/dashboard/cli-tools/**`.

## Composition
- `CLIToolsPageClient` orchestrates card components per tool family.
- Components include dedicated cards for Claude, Codex, Cline, OpenClaw, Copilot, Droid, Kilo, Antigravity, MITM, and Cowork.

## API coupling
- Cards call `/api/cli-tools/**` routes to write/read local client configuration payloads.
