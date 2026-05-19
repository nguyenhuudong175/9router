# 9Router internals (reverse-engineering notes)

## 1) Core mental model

9Router is a **local compatibility gateway** that makes many providers look like one OpenAI-style endpoint, but its real internal architecture is:

1. **Next.js API surface** (`src/app/api/*`) for dashboard + public `/v1` compatibility.
2. **Protocol core** (`src/sse/*` + `open-sse/*`) for model resolution, auth/account selection, translation, execution, streaming normalization, and usage capture.
3. **Local control plane** (SQLite + settings + process manager) that tracks provider accounts, model aliases/combos, pricing, observability, tunnels, and MITM state.

Important: most user-visible APIs are thin wrappers; the behavior lives in the `handleChat -> handleChatCore` path.

---

## 2) Runtime boot sequence and process-level behavior

### What initializes first

- `open-sse/index.js` patches global `fetch` immediately (proxy + DNS-bypass logic).
- `src/lib/initCloudSync.js` auto-runs `initializeApp()` via `setImmediate`, except in build phase.
- `initializeApp()` does much more than “cloud sync”: it starts background lifecycle services.

### What `initializeApp()` actually does

- Cleans invalid provider rows (`cleanupProviderConnections`).
- Auto-resumes tunnel and tailscale if settings say enabled.
- Boots MITM (if enabled and password is available), restores DNS rewrites.
- Installs signal handlers to remove DNS entries and kill cloudflared on exit.
- Starts watchdog + network monitors that trigger safe reconnect flows.

### Hidden engineering idea

The app is designed to survive Next.js dev/HMR module reloads via `globalThis` singletons (`__appSingleton`, `__cloudSyncInit`, `_dbAdapter`, pending request globals).  
This is a deliberate “state outside module cache” strategy to avoid duplicate schedulers and reinitialization storms.

---

## 3) Request execution path (`/v1/chat/completions`, `/v1/messages`, `/v1/responses`)

## Entry and endpoint strategy

- `/v1/*` rewrites to `/api/v1/*` in `next.config.mjs`.
- Chat/messages/responses routes all call `handleChat()` and only differ by incoming format.
- Translator registry is lazy-loaded once (`initTranslators()` guard).

## Real flow inside `handleChat`

1. Parse body + request metadata logging.
2. Optional API key enforcement (`settings.requireApiKey` + DB validation).
3. Early bypass for Claude CLI warmup/naming probes (`handleBypassRequest`) to avoid wasting account/combo rotation.
4. Resolve combo or single model.
5. For single model, repeatedly:
   - pick account via provider strategy,
   - refresh tokens if needed,
   - call `handleChatCore`,
   - on failure, lock account/model and fallback to next account.

### Account fallback mechanics

- Not “provider down” globally; it is **per-connection + per-model lock** (`modelLock_<model>` flat fields).
- Error classification is config-driven (`ERROR_RULES`), with exponential backoff and optional provider reset timestamps.
- Success clears current model lock and lazily clears expired locks.

This gives fine-grained degradation: one bad account/model can cool down while others keep serving.

---

## 4) Translation + execution core (`handleChatCore`)

`handleChatCore` is the system’s critical transformer/orchestrator:

1. Detect source format from body/endpoint.
2. Resolve provider target format (plus per-model target format overrides).
3. Apply optional provider thinking override.
4. Decide stream/non-stream considering client headers and tool quirks.
5. Optionally run **native passthrough** (no translation when client ecosystem matches provider).
6. Otherwise translate through registry.
7. Apply request-level transforms:
   - tool dedupe (Claude),
   - RTK compression of tool-result payloads,
   - caveman prompt injection.
8. Execute provider adapter.
9. Handle 401/403 refresh-and-retry.
10. Normalize stream/non-stream response and persist usage + request detail.

### High-value hidden tricks

- **Two-step translator graph**: source -> OpenAI -> target (reduces translator matrix complexity).
- **Native passthrough mode**: avoids fidelity loss for same-ecosystem tool/provider pairs.
- **Tool cloaking/decloaking** for Claude OAuth traffic (`_cc` remap) to avoid policy-sensitive tool-name behavior.
- **Forced SSE-to-JSON bridge** for providers requiring stream even when client asked for JSON.

---

## 5) Provider adapter architecture

- `getExecutor(provider)` returns specialized adapters when needed; unknown providers use cached `DefaultExecutor`.
- Compatible providers are represented as synthetic provider IDs (`openai-compatible-*`, `anthropic-compatible-*`) with runtime URL/header logic.
- Provider headers are intentionally opinionated per upstream (e.g., GitHub Copilot VSCode-like headers).

Engineering decision: keep protocol adaptation mostly in `services/provider.js` and executor classes so route code stays thin.

---

## 6) Model resolution, aliases, combos, and capability slicing

### Resolution layers

1. Parse `alias/model` or direct provider ID.
2. Resolve local alias map from DB.
3. Check provider-node prefixes (for user-defined compatible nodes).
4. If bare name, treat as potential combo before alias fallback.

### Combo behavior

- Combo mode supports strategy: fallback or round-robin with sticky limit.
- Rotation state is in-memory map keyed by combo name.
- Transient provider errors can intentionally wait a short cooldown before trying next model (reduces over-eager failover).

### Model listing

`/v1/models` and `/v1/models/{kind}` build model sets from:

- active connections,
- static provider model map,
- custom models,
- aliases,
- disabled model filters,
- dynamic fetch for compatible providers if needed.

This yields capability-aware model catalogs (llm/image/tts/stt/embedding/web/etc.).

---

## 7) Persistence and data migration model

Current persistence is SQLite-first:

- file: `${DATA_DIR}/db/data.sqlite`
- layered adapters: bun sqlite -> better-sqlite3 -> node:sqlite -> sql.js fallback.
- DB initialization is global singleton + single init promise.

### Migration strategy

- Versioned migration chain + additive schema sync.
- One-time JSON import from legacy files if DB is fresh (`db.json`, `usage.json`, etc.).
- Marker file prevents repeated imports.
- Backup policy around imports and version upgrades.

### Design pattern worth reusing

Repository modules expose backward-compatible shims (`localDb.js`, `usageDb.js`) so old callers survive large storage refactors.

---

## 8) Observability and usage accounting

Two observability lanes:

1. **Usage stats** (`usageRepo`):
   - tracks pending requests in-memory,
   - writes history + daily aggregates + lifetime counters transactionally,
   - serves dashboard SSE stream updates.
2. **Request details** (`requestDetailsRepo`):
   - buffered batched writes,
   - configurable retention and payload truncation,
   - sensitive header stripping.

Notable behavior: if provider usage is missing, system estimates tokens and still tracks cost/metrics continuity.

---

## 9) Security and trust boundaries

### Auth layers

- Dashboard JWT cookie auth via middleware gate.
- Optional API key requirement for `/v1` endpoints (checked in chat handler).
- Local-only restrictions for routes that can spawn processes or touch host secrets.
- CLI-token bypass for protected routes via machine-id-derived token header.

### Transport and proxy controls

- Proxy selection hierarchy: per-connection proxy -> env proxy.
- NO_PROXY matching implemented.
- MITM bypass hosts use Google DNS resolution + direct socket path to avoid local DNS poisoning.

This is an unusual but intentional host-defense pattern for known interception-sensitive endpoints.

---

## 10) Tunnel + MITM + updater subsystems (ops plane)

These are not side features; they are integrated into startup and failure recovery.

- Tunnel manager orchestrates cloudflared and tailscale, with health checks and reconnect guards.
- MITM manager handles cert lifecycle, privileged DNS host edits, encrypted sudo password storage, and auto-restore.
- Updater spawns detached runtime updater, kills sibling processes to release lock-sensitive files (especially Windows), and relaunches safely.

Key decision: runtime-copy critical scripts (MITM server/updater) into data dir to avoid `npm -g` lock/update conflicts.

---

## 11) Frontend interaction pattern

UI is mostly a control plane over APIs:

- Zustand stores with short TTL cache (`CLIENT_STORE_TTL_MS`) reduce request spam.
- Dashboard pages are thin wrappers around client components.
- Most UI state mutates through API routes, not direct local state logic.

So backend route behavior is the real source of truth; UI mainly reflects it.

---

## 12) Reusable implementation patterns extracted from this repo

1. **Single canonical core handler** for many API variants (messages/completions/responses).
2. **Format-bridge architecture** through a pivot format (OpenAI) to avoid NxN translators.
3. **Per-account, per-model circuit-breaker** instead of global provider disable.
4. **Startup idempotence with global singletons** in hot-reload runtimes.
5. **Backward-compatibility shims** during data-layer rewrites.
6. **Operational hardening in app code** (tunnel watchdogs, DNS restore, updater lock handling).

---

## 13) Where to read first next time (fast re-entry map)

1. `src/sse/handlers/chat.js`
2. `open-sse/handlers/chatCore.js`
3. `open-sse/translator/index.js`
4. `open-sse/services/provider.js`
5. `src/sse/services/auth.js`
6. `src/lib/db/driver.js`, `src/lib/db/migrate.js`, `src/lib/db/repos/*`
7. `src/shared/services/initializeApp.js`
8. `src/lib/tunnel/tunnelManager.js`
9. `src/mitm/manager.js`
10. `cli/cli.js`

If these files are understood, most repository behavior becomes predictable.

