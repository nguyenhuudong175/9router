# Provider Management APIs

## Core endpoints
- `/api/providers` list/create connections (`src/app/api/providers/route.js`).
- `/api/providers/[id]` update/delete and `/test`, `/models`, `/test-models` subroutes.
- `/api/provider-nodes` manages compatible upstream node definitions.

## Input normalization
- Provider IDs and provider-specific payloads normalized by `src/lib/providerNormalization.js`.
- Connection proxy settings validated and folded into `providerSpecificData`.

## Data safety
- Sensitive credentials are removed from GET responses (`apiKey`, `accessToken`, `refreshToken`).
