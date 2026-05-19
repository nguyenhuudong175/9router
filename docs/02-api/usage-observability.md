# Usage and Observability APIs

## Usage endpoints
- `/api/usage/stats`, `/chart`, `/history`, `/logs`, `/stream`, `/request-logs`, `/request-details`, `/[connectionId]`.

## Backing storage
- Usage metrics and request details are backed by DB repository functions exported through `src/lib/db/index.js`.

## Streaming status
- Active request tracking and status emitters originate from usage repo (`statsEmitter`, `trackPendingRequest`).
