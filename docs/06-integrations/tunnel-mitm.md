# Tunnel + MITM Integration

## Initialization controller
- `initializeApp()` in `src/shared/services/initializeApp.js` handles auto-resume and process lifecycle hooks.

## Tunnel resilience
- Watchdog and network monitor loops call safe restart functions for tunnel and tailscale services.
- Restart guards include cooldown, spawn lock, internet probe, and service-alive checks.

## MITM coupling
- MITM manager DB hooks are initialized from ESM context.
- Auto-start can restore DNS entries and uses active API key for startup parameters.
