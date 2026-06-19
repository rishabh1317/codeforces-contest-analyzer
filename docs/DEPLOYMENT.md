# Deployment Guide

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./app.db` | SQLAlchemy connection string |
| `CF_API_BASE` | `https://codeforces.com/api` | Codeforces API base URL |

### Frontend (`frontend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API URL |

## Local Production Build

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend && npm install && npm run build
npx serve dist -l 5173
```

## Docker (Example)

```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build frontend separately and serve static files via nginx or CDN, pointing `VITE_API_BASE_URL` to your API host.

## Production Recommendations

1. **Database** — Use PostgreSQL: `DATABASE_URL=postgresql://user:pass@host/db`
2. **CORS** — Set `cors_origins` in `config.py` / env to your frontend domain only
3. **HTTPS** — Terminate TLS at reverse proxy (nginx, Caddy, cloud load balancer)
4. **Caching** — Add Redis for shared cache across instances
5. **Monitoring** — Log aggregation for CF API failures and slow requests

## Database Migrations

Alembic is configured (`backend/alembic.ini`). For schema changes:

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

Current schema is auto-created via `Base.metadata.create_all()` on startup.
