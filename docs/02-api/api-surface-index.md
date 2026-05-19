# API Surface Index

## Compatibility APIs
- `src/app/api/v1/**`: chat, messages, responses, embeddings, models, audio, images, search, web fetch.
- `src/app/api/v1beta/models/**`: beta model listing pass-through.

## Dashboard management APIs
- Providers, nodes, keys, combos, pricing, settings, usage, tags.
- OAuth and cloud-related handlers under `/api/oauth/**` and `/api/cloud/**`.
- CLI tools, tunnel controls, MCP bridge, translator utilities.

## Security gate
- Most `/api/*` routes are guarded by `src/dashboardGuard.js` with public allow-list + JWT/CLI token checks.
