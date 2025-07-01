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

Start all containers:

```bash
docker compose up -d
```

Visit `http://localhost:3000` to complete the setup. The installer
allows you to create the admin account and enter API keys for
Whisper, OpenAI and ElevenLabs.
All configuration values are stored in Redis so containers can start
without additional environment variables.

## Development

Each service has its own `Dockerfile` and lightweight source code. The actual API calls to Whisper, OpenAI and ElevenLabs are placeholders that need real credentials and error handling. This setup is intended as a starting point for further development.
