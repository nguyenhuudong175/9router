# Translation Pipeline

## Registry architecture
- Translators are registered lazily in `open-sse/translator/index.js`.
- Separate request and response registries use key pairs `${from}:${to}`.

## Request translation path
- Source format detected by payload/endpoint (`detectFormat`, `detectFormatByEndpoint`).
- Conversion pipeline: `source -> openai -> target` when needed.
- OpenAI target requests are normalized via `filterToOpenAIFormat`.
- Claude target requests pass through `prepareClaudeRequest`.

## Response translation path
- Stream chunks convert `target -> openai -> source`.
- Stateful handling supports OpenAI Responses API sequencing fields.
