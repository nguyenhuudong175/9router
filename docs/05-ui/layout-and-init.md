# UI Layout and App Initialization

## Root layout responsibilities
- Global CSS/font setup and provider wrappers in `src/app/layout.js`.
- Auto-imports initialization modules: cloud sync, outbound proxy env, console log capture.

## Initialization path
- `src/lib/initCloudSync.js` ensures singleton app init and invokes `initializeApp()`.
- `initializeApp()` performs provider cleanup, tunnel/mitm auto-resume, watchdog and network monitor startup.
