# TAKWEEN — Render Ready

This package is prepared for a Render Docker Web Service.

## GitHub
Upload the **contents of this folder** to the root of your GitHub repository.
The repository root must contain:

- `Dockerfile`
- `render.yaml`
- `requirements.txt`
- `backend/`
- `frontend/`
- the TAKWEEN engine `.py` files

Do not upload the ZIP as the repository root.

## Render
1. New → Web Service.
2. Connect the GitHub repository.
3. Language: Docker.
4. Dockerfile Path: `./Dockerfile`.
5. Docker Context: `.`.
6. Plan: Free (for testing).
7. Health Check Path: `/health`.
8. Deploy.

Render provides `PORT` at runtime (default 10000). The Docker command binds to `0.0.0.0` and uses `$PORT`.

## Test URLs
After deployment:
- `/` — TAKWEEN web UI
- `/health` — health check
- `/docs` — FastAPI API documentation
- `/platform/manifest` — platform manifest

## Important
The Free Render service is for testing/MVP use. It can sleep when idle and has resource/storage limitations. Do not use it as the production data store for customer projects.
