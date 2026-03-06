# AI APK Generator (API-only mode)

This service now runs as a **standalone FastAPI API** without requiring Celery, Redis, PostgreSQL, or Flower.

## Prerequisites
- Docker Desktop (or Docker Engine + Compose plugin)
- Poetry
- Python 3.12+

## Quick start

### 1) Run from Docker Compose (`infra/`)
```bash
cd infra
docker compose up --build
```
This starts only one container: `aiapk-api`.

### 2) Run directly with Poetry (`ai-service/`)
```bash
cd ai-service
poetry install
poetry run uvicorn app.main:app --reload
```

Open:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health/live`

## Windows Docker Desktop error
If you see:

`open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`

Then Docker Desktop engine is not running. Fix it by:
1. Start Docker Desktop and wait until "Engine running".
2. Ensure Linux containers mode is enabled.
3. Verify:
   - `docker version`
   - `docker context ls` (use `desktop-linux`)
4. Re-run:
   - `docker compose up --build`
