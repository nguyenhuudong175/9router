# Media Endpoints

## LLM-adjacent media APIs
- TTS voices and speech generation under `/api/v1/audio/**` and `/api/media-providers/tts/**`.
- STT transcription endpoint: `/api/v1/audio/transcriptions`.
- Image generation endpoint: `/api/v1/images/generations`.
- Embeddings endpoint: `/api/v1/embeddings`.

## Core implementation modules
- `open-sse/handlers/ttsCore.js`, `sttCore.js`, `imageGenerationCore.js`, `embeddingsCore.js`.
- Provider plugins in `open-sse/handlers/{ttsProviders,imageProviders,embeddingProviders}/`.
