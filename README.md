# WhisperAI API Container

A containerized API for OpenAI's Whisper speech-to-text model with the ability to dynamically switch models.

## Features

- Speech-to-text transcription using OpenAI's Whisper model
- Dynamic model switching via API endpoint
- Support for multiple model sizes (tiny, base, small, medium, large)
- Docker container for easy deployment
- Health check endpoint
- GPU acceleration support (when available)

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- CUDA-compatible GPU (optional, for GPU acceleration)

### Building and Running with Docker Compose

```bash
# Build and start the container
docker-compose up -d

# Check logs
docker-compose logs -f
```

### API Endpoints

#### Health Check

```
GET http://localhost:5000/
```

Response:
```json
{
  "status": "ok",
  "device": "cpu",  # or "cuda" if GPU is available
  "current_model": "base"
}
```

#### Get Model Information

```
GET http://localhost:5000/model
```

Response:
```json
{
  "current_model": "base",
  "available_models": ["tiny", "base", "small", "medium", "large"],
  "device": "cpu"  # or "cuda" if GPU is available
}
```

#### Change Model

```
POST http://localhost:5000/model
Content-Type: application/json

{
  "model": "tiny"
}
```

Response:
```json
{
  "message": "Model changed to tiny",
  "current_model": "tiny"
}
```

#### Transcribe Audio

```
POST http://localhost:5000/whisper
Content-Type: multipart/form-data

file=@your_audio.wav
```

Response:
```json
{
  "filename": "your_audio.wav",
  "text": "This is the transcribed text.",
  "model": "tiny"
}
```

## Model Sizes and Performance

| Model | Size | Memory Required | Speed | Accuracy |
|-------|------|----------------|-------|----------|
| tiny  | 39M  | Low            | Fast  | Basic    |
| base  | 74M  | Low            | Fast  | Good     |
| small | 244M | Medium         | Medium| Better   |
| medium| 769M | High           | Slow  | High     |
| large | 1.5G | Very High      | Slow  | Highest  |

Choose the model size based on your hardware constraints and accuracy requirements.

## GPU Support

The container automatically detects and uses CUDA-compatible GPUs if available. You can verify GPU usage through the health check endpoint, which will show `"device": "cuda"` when a GPU is being used.

To check GPU availability before running the container, use:

```bash
python check_gpu.py
```

## Development

To modify the application during development, you can uncomment the volume mount in `docker-compose.yml`:

```yaml
volumes:
  - ./app.py:/app/app.py
```

This allows you to modify the `app.py` file and have the changes reflected in the container.

## Testing

You can test the API with curl:

```bash
# Health check
curl http://localhost:5000/

# Change model
curl -X POST http://localhost:5000/model \
  -H "Content-Type: application/json" \
  -d '{"model": "tiny"}'

# Transcribe audio
curl -X POST http://localhost:5000/whisper \
  -F "file=@test/TimCurry.wav"
```

You can also use the test script provided:

```bash
python test/test_container_api.py
```

## Last Updated

October 4, 2023
