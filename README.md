# Codeforces Contest Analyzer

A full-stack analytics platform that turns Codeforces contest and submission history into actionable insights — weak topic detection, personalized problem recommendations, contest performance analytics, rival comparison, and rating growth prediction.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)

## Features

| Feature | Description |
|---------|-------------|
| **Weak Topic Detection** | Per-tag attempts, solves, success rate, avg difficulty, and relative performance score |
| **Problem Recommendations** | Personalized problems from the CF problemset based on weak tags and rating |
| **Contest Analytics** | Rating timeline, rank trends, consistency, upsolve stats, contest frequency |
| **Rival Comparison** | Side-by-side stats, growth trends, topic strengths, automated insights |
| **Rating Predictor** | Linear regression on contest history with confidence score and improvement tips |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

Optional: set `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env`

## Architecture

```
┌─────────────┐     REST API      ┌──────────────────────────────────┐
│  React SPA  │ ◄──────────────► │  FastAPI                         │
│  (Vite)     │                   │  ├── routers/ (api, analysis)    │
│             │                   │  ├── services/                   │
│  Dashboard  │                   │  │   ├── topic_analyzer           │
│  Compare    │                   │  │   ├── recommendation_engine    │
│  Charts     │                   │  │   ├── contest_analytics        │
└─────────────┘                   │  │   ├── rating_predictor         │
                                  │  │   ├── codeforces (CF API)      │
                                  │  │   └── cache_service            │
                                  │  ├── SQLAlchemy + SQLite           │
                                  │  └── AnalysisCache / ContestCache  │
                                  └──────────────┬───────────────────┘
                                                 │
                                    Codeforces Public API
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## API Overview

| Endpoint | Description |
|----------|-------------|
| `GET /api/users/{handle}/dashboard` | Full dashboard payload (single optimized call) |
| `GET /api/users/{handle}/tag-analysis` | Per-tag statistics |
| `GET /api/users/{handle}/contest-analytics` | Contest performance metrics |
| `GET /api/users/{handle}/recommendations` | Personalized problem list |
| `GET /api/users/{handle}/rating-prediction` | Rating growth forecast |
| `GET /api/compare?handle1=&handle2=` | Rival comparison |
| `GET /analysis/codeforces/{handle}` | Legacy analysis endpoint |

Full reference: [docs/API.md](docs/API.md)

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment with Docker, environment variables, and database migration notes.

## Testing

```bash
cd backend
python test_backend.py
python test_features.py
```

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app entry
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic response models
│   ├── routers/             # API route handlers
│   └── services/            # Business logic layer
├── frontend/
│   └── src/
│       ├── api/             # Axios client
│       ├── components/      # Dashboard, Charts, SearchBar
│       ├── hooks/           # useUserStats
│       └── pages/           # Home, Dashboard, Compare
└── docs/                    # Architecture, API, deployment guides
```

## License

MIT
