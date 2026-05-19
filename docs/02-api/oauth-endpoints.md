# OAuth Endpoints

## Generic OAuth handler
- `/api/oauth/[provider]/[action]` handles provider action dispatch.

## Provider-specific routes
- Cursor import/auto-import.
- Kiro import/social authorize/social exchange/auto-import.
- iFlow cookie import and GitLab PAT route.

## Service layer
- Implementations are split under `src/lib/oauth/services/*` with shared constants/utilities in `src/lib/oauth/constants` and `src/lib/oauth/utils`.
