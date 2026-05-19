# OAuth Service Layer

## Module set
- `src/lib/oauth/services/*` includes per-provider implementations and shared base logic.
- Common helpers in `src/lib/oauth/utils/{server,ui,pkce,banner}.js`.

## Covered providers (service files present)
- claude, codex, cursor, gemini, github, iflow, kiro, openai, qoder, qwen, antigravity.

## API entrypoints
- Generic dynamic route: `/api/oauth/[provider]/[action]`.
- Additional import/social routes for cursor/kiro providers.
