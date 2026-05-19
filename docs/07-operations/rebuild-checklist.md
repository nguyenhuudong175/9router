# Rebuildability Checklist

1. Install root dependencies (`npm install`) and ensure Next binary is available.
2. Confirm environment variables (`DATA_DIR`, `PORT`, `NEXT_PUBLIC_BASE_URL`, secrets).
3. Build with `npm run build`.
4. Start with `npm run start` (or Docker runtime).
5. Verify health and auth bootstrap endpoints (`/api/health`, `/api/settings`, `/api/version`).
6. Add provider connection and run `/api/providers/[id]/test`.
7. Send sanity request to `/v1/chat/completions`.
8. Verify usage telemetry routes return data.
