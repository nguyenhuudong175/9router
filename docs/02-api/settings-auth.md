# Settings and Auth APIs

## Settings API
- `GET/PATCH /api/settings` in `src/app/api/settings/route.js`.
- Password change path verifies previous hash then stores bcrypt hash.
- Proxy-related changes immediately update process env through `applyOutboundProxyEnv`.

## Auth routes
- `/api/auth/login`, `/api/auth/logout`, `/api/auth/status`.
- OIDC routes under `/api/auth/oidc/{start,callback,test}`.

## Session mechanics
- JWT cookie issuance/verification in `src/lib/auth/dashboardSession.js`.
