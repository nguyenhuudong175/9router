# Tunnel Endpoints

## Tunnel API set
- `/api/tunnel/enable`, `/disable`, `/status`.
- Tailscale helpers: `/tailscale-install`, `/tailscale-enable`, `/tailscale-disable`, `/tailscale-check`, `/tailscale-login`, `/tailscale-start-daemon`.

## Runtime controller
- Backed by `src/lib/tunnel/tunnelManager.js` and service-specific modules (`cloudflared.js`, `tailscale.js`).

## Middleware constraints
- Installation and some local-machine operations are loopback-only via `LOCAL_ONLY_PATHS` checks.
