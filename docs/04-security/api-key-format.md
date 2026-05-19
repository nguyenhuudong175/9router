# API Key Format

## Generator
- `src/shared/utils/apiKey.js` creates key format: `sk-{machineId}-{keyId}-{crc8}`.

## Integrity check
- CRC segment is derived from HMAC-SHA256(secret, machineId+keyId), truncated to 8 hex chars.
- Secret source: `API_KEY_SECRET` env, with built-in fallback string.

## Backward compatibility
- Legacy two-part keys (`sk-{random}`) are still parsed as valid old format.
