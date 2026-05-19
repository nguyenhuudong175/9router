# open-sse Module Map

## Core directories
- `handlers/`: chat/media/search/fetch core handlers.
- `executors/`: provider-specific network adapters.
- `translator/`: format transformations request/response.
- `services/`: provider/model/fallback/token helper logic.
- `utils/`: stream/proxy/error/request-logging helpers.
- `rtk/`: tool-result compression filters and utilities.
- `config/`: provider model constants and runtime settings.

## Entrypoint
- `open-sse/index.js` wires module exports for runtime use by `src/sse` handlers.
