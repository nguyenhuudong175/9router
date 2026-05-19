# Auth and Session

## Dashboard auth token
- Implemented in `src/lib/auth/dashboardSession.js` using HS256 JWT via `jose`.
- JWT secret is loaded from `JWT_SECRET` or generated into `${DATA_DIR}/jwt-secret` (mode `0600`).

## Cookie behavior
- Cookie name: `auth_token`.
- `httpOnly`, `sameSite=lax`, path `/`.
- `secure` is enabled when `AUTH_COOKIE_SECURE=true` or `x-forwarded-proto=https`.

## Login policy
- Middleware can bypass dashboard login if `requireLogin=false` in settings.
