# MCP and Translator Endpoints

## MCP bridge
- `/api/mcp/[plugin]/sse` and `/api/mcp/[plugin]/message`.
- Uses stdio/SSE bridge utilities under `src/lib/mcp/stdioSseBridge.js`.

## Translator routes
- `/api/translator/{load,save,translate,send}` plus console log stream routes.

## Intended role
- Supports local tooling integrations and translation debugging workflows exposed in dashboard pages.
