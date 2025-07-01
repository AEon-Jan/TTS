# TTS Streaming Bot

This repository contains a modular Docker setup for a Twitch text-to-speech bot. The architecture uses separate services for speech-to-text, language model processing, text-to-speech synthesis and a small control panel.

**Services**

- `gateway` – central FastAPI service that exposes REST endpoints and manages queues in Redis.
- `stt-client` – captures audio and sends it to a speech‑to‑text API.
- `llm-worker` – consumes messages from Redis, calls the OpenAI API and stores the result.
- `tts-worker` – converts text to audio via the ElevenLabs API and provides a URL for playback.
- `panel` – minimal React UI for monitoring and control.
- `redis` – message queue.
- `minio` – optional caching of generated audio.

The stack is built to run on a GPU‑less Debian 12 VM.

## Quick start

1. Copy `.env.example` to `.env` and adjust all secrets.
2. Build and start the services:

```bash
docker compose up --build
```

The panel will be available on `http://localhost:3000`.

## Development

Each service has its own `Dockerfile` and lightweight source code. The actual API calls to Whisper, OpenAI and ElevenLabs are placeholders that need real credentials and error handling. This setup is intended as a starting point for further development.
