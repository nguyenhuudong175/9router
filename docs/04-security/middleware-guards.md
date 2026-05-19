# Middleware Guards

## Guard implementation
- `src/dashboardGuard.js` is applied via `src/proxy.js` matcher.

## Control layers
- Public path allow-list for health/init/auth/version and `/v1` APIs.
- Always-protected paths require valid JWT or machine-derived CLI token.
- `/api/*` defaults to deny unless authenticated.
- Sensitive local-only routes require loopback host/origin matching.

## Dashboard behavior
- `/dashboard/**` redirects to `/login` when login required and token invalid/missing.
