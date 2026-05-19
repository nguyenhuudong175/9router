# Testing Strategy (Current)

## Existing suite
- Dedicated tests package under `tests/`.
- Command: `npm test` in `tests/` executes Vitest with explicit `/tmp/node_modules` path.

## Scope in repository
- Current documented tests target embeddings flow (`tests/unit/embeddingsCore.test.js`).
- Additional cloud embeddings tests are referenced by tests README.

## Practical implication
- High-coverage unit tests are concentrated in embeddings subsystem; broader API/runtime paths rely more on runtime validation.
