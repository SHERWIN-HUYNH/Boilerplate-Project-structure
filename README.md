# Boilerplate

This repository contains a Next.js frontend and a FastAPI backend boilerplate for AI interview projects.

## Backend

See `backend/README.md` for backend-specific usage.

## Docker

### Run backend

```bash
docker compose up --build
```

The backend will be available at `http://localhost:8000`.

### First-time setup

1. Copy `backend/.env.example` to `backend/.env`
2. Adjust values if needed
3. Run `docker compose up --build`
