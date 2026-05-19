# Secrets and Risk Surfaces

## Secret-bearing surfaces
- Provider credentials in `providerConnections.data` blobs.
- JWT secret file in data directory.
- API key secret and machine-id salt from environment.

## Potentially risky defaults
- Password bootstrap behavior includes handling for initial default (`123456`) in settings update flow.
- Provider config table includes embedded client IDs/secrets for some OAuth-like integrations (`open-sse/config/providers.js`).

## Operational hardening priorities
- Enforce custom secrets in deployment env.
- Protect filesystem permissions for `${DATA_DIR}`.
- Restrict dashboard exposure when tunnel access is enabled.
