# 9Router Repository Overview

## Purpose
9Router is a local AI gateway and dashboard that exposes OpenAI-compatible endpoints (`/v1/*`) while routing traffic to many upstream providers with translation, fallback, usage tracking, and provider/account management.

## High-level layout
- `src/app/`: Next.js App Router UI + API routes.
- `src/sse/`: request entry handlers, auth/model resolution, logging helpers.
- `open-sse/`: shared execution core (translation, executors, streaming, retries, media/search handlers).
- `src/lib/db/`: SQLite-backed persistence layer, migration, repositories.
- `src/shared/`: shared constants/services used by route and runtime layers.
- `tests/`: Vitest-based unit/e2e-style tests for routing, translation, DB, and provider behavior.
- `docs/`: technical documentation.

## Runtime model
1. Client sends requests to `/v1/*`.
2. Next.js routes map to handlers under `src/app/api/v1/*`.
3. Handlers delegate to `src/sse/handlers/*`.
4. Core request execution happens in `open-sse/handlers/*` + provider executors.
5. Config/state is loaded from SQLite via `src/lib/db/*`.
6. Usage and request details are persisted and exposed through `/api/usage/*`.

## Primary capabilities
- OpenAI-compatible chat/responses/messages/models endpoints.
- Multi-provider routing with account fallback and combo model fallback.
- Request/response translation across formats (OpenAI, Claude, Gemini, etc.).
- Streaming and non-streaming handling, including forced SSE-to-JSON conversion paths.
- Media/search endpoints (embeddings, image generation, TTS/STT, web search/fetch).
- Dashboard APIs for providers, OAuth/API-key setup, settings, pricing, aliasing, and sync.

## Technology stack
- Next.js 16 + React 19.
- Node.js runtime (Dockerfile uses Node 22 Alpine).
- SQLite with adapter fallback (`better-sqlite3` / `node:sqlite` / `sql.js`, Bun path supported).
- SSE-based streaming pipeline with translator/executor architecture.
