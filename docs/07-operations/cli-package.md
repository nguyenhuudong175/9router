# CLI Package Notes

## Package metadata
- `cli/package.json` defines published package `9router` with bin `9router -> ./cli.js`.

## Runtime strategy
- CLI comments document deferred runtime installation of sqlite/systray dependencies into `~/.9router/runtime/node_modules` to avoid global install lock issues.

## Build flow
- CLI build script: `node scripts/build-cli.js`.
- Postinstall hook executes `node hooks/postinstall.js`.
