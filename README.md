# Whisper Server (Docker)

A Whisper transcription service using `faster-whisper` that exposes an OpenAI-compatible API. Runs on any platform via Docker (CPU-only, no GPU required).

This is the Docker/Railway-deployable counterpart to [whisper-server-apple-silicon](https://github.com/chaosslabs/whisper-server-apple-silicon).

## Quick Start

### Docker

```bash
docker build -t whisper-server .
docker run -p 8080:8080 whisper-server
```

The model (`large-v3-turbo`) is downloaded on first startup and cached inside the container. To persist the cache across restarts:

```bash
docker run -p 8080:8080 -v whisper-cache:/root/.cache whisper-server
```

### Railway

Deploy directly from this repo. Railway will use the Dockerfile automatically. No additional configuration needed — the server listens on port 8080 by default.

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_SERVER_HOST` | `0.0.0.0` | Host to bind to |
| `WHISPER_SERVER_PORT` | `8080` | Port to listen on |

## API Usage

### Transcribe Audio

```bash
curl -X POST http://localhost:8080/v1/audio/transcriptions \
  -F "file=@audio.mp3"
```

Response:
```json
{"text": "Transcribed text here..."}
```

### Health Check

```bash
curl http://localhost:8080/health
```

## Model

Uses `large-v3-turbo` via [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2 backend). The model is downloaded from Hugging Face on first use and cached in `~/.cache/huggingface`.

## License

MIT
