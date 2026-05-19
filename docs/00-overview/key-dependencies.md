# Key Dependencies

## Application dependencies
- Core framework: `next`, `react`, `react-dom`.
- Auth/security: `jose`, `bcryptjs`.
- Networking/proxy: `undici`, `http-proxy-middleware`, `socks-proxy-agent`.
- Data layer fallback: optional `better-sqlite3`, plus `sql.js` fallback (`package.json`, `src/lib/db/adapters/*`).

## Developer dependencies
- Linting: `eslint`, `eslint-config-next`.
- Styling/tooling: `tailwindcss`, `postcss`.

## Test dependencies
- Tests package uses `vitest` from `/tmp/node_modules` path (`tests/package.json`).
