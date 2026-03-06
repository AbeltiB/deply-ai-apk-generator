# AI APK Generator (API-only mode)

This service runs as a **standalone FastAPI API** without requiring Celery, Redis, PostgreSQL, or Flower.

## Prerequisites
- Docker Desktop (or Docker Engine + Compose plugin)
- Poetry
- Python 3.12+

## Atomic step-by-step flow (your desired workflow)

### Step 1 — start the API
Option A (Docker):
```bash
cd infra
docker compose up --build
```

Option B (Poetry):
```bash
cd ai-service
poetry install
poetry run uvicorn app.main:app --reload
```

### Step 2 — send a generate request
```bash
curl -X POST http://127.0.0.1:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a todo app with add/delete/complete",
    "user_id": "debug-user"
  }'
```

You will receive a `task_id`.

### Step 3 — watch processing in console
When request starts, console logs show events like:
- `api.generation.started`
- `api.generation.pipeline_completed`
- `api.generation.completed`

### Step 4 — check task progress/status
```bash
curl http://127.0.0.1:8000/api/v1/task/<TASK_ID>
```

### Step 5 — get converted result JSON
```bash
curl http://127.0.0.1:8000/api/v1/results/<TASK_ID>
```

### Step 6 — get export JSON for your downstream system
```bash
curl http://127.0.0.1:8000/api/v1/results/<TASK_ID>/export
```

### Step 7 — download export JSON file (attachment)
```bash
curl -OJ http://127.0.0.1:8000/api/v1/results/<TASK_ID>/download
```

> Note: `/results/{task_id}` and export/download endpoints now attempt inline recovery for stuck queued/processing tasks (when recoverable payload exists), so you can still obtain final JSON for testing.

## Windows Docker Desktop error
If you see:

`open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`

Then Docker Desktop engine is not running. Fix it by:
1. Start Docker Desktop and wait until **Engine running**.
2. Ensure Linux containers mode is enabled.
3. Verify:
   - `docker version`
   - `docker context ls` (use `desktop-linux`)
4. Re-run:
   - `docker compose up --build`
