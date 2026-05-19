# RTK + Caveman Request Mutations

## RTK compression
- Applied in `chatCore` before executor dispatch using `compressMessages` (`open-sse/rtk/index.js`).
- Targets tool-result payload shapes in OpenAI, Claude, and OpenAI Responses messages.
- Skips too-small or too-large blobs and avoids output growth.

## Caveman prompt mode
- Controlled by settings flags (`cavemanEnabled`, `cavemanLevel`) passed from `src/sse/handlers/chat.js`.
- Injects terse system guidance via `injectCaveman` before upstream call.

## Logging
- RTK emits summary line: saved bytes and applied filters.
