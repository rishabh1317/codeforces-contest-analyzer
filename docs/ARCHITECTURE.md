# Architecture

## Design Principles

1. **Service layer separation** — Routers handle HTTP; services contain analytics logic.
2. **Single dashboard endpoint** — `/api/users/{handle}/dashboard` aggregates all data with shared caching to minimize Codeforces API calls.
3. **Layered caching** — In-memory TTL cache (5 min) for CF API responses + SQLite `AnalysisCache` for submission payloads.

## Backend Layers

### Routers (`backend/routers/`)

| Router | Prefix | Role |
|--------|--------|------|
| `api.py` | `/api` | Primary REST API — dashboard, analytics, compare |
| `analysis.py` | `/analysis` | Legacy-compatible analysis endpoint |
| `users.py` | `/users` | User record lookup from local DB |

### Services (`backend/services/`)

| Service | Responsibility |
|---------|----------------|
| `codeforces.py` | Async HTTP client for Codeforces API with in-memory cache |
| `cache_service.py` | DB-backed submission cache + user profile sync |
| `topic_analyzer.py` | Tag-level statistics, weak/strong topic ranking |
| `recommendation_engine.py` | Problem scoring from CF problemset |
| `contest_analytics.py` | Rating timeline, consistency, upsolve metrics |
| `rating_predictor.py` | Linear regression rating forecast |

### Data Flow

```
User Request → Router → cache_service (submissions from DB or CF API)
                       → topic_analyzer / contest_analytics / etc.
                       → Pydantic schemas → JSON response
```

## Database

SQLite by default (`sqlite:///./app.db`). Tables:

- **users** — Cached handle, rating, max_rating
- **analysis_cache** — Full submission JSON per handle (5-min TTL logic in service)
- **contest_cache** — Participant counts per contest ID
- **problems / submissions** — Schema present for future normalization (not actively populated)

## Frontend

- **React 19 + Vite** — SPA with React Router
- **Tailwind CSS** — Dark analytics theme with glass-morphism panels
- **Recharts** — Bar, radar, line, area charts
- **useUserStats hook** — Single dashboard fetch, maps to Dashboard component props

### Pages

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | HomePage | Handle search entry |
| `/dashboard/codeforces/{handle}` | DashboardPage | Full analytics dashboard |
| `/compare` | ComparePage | Two-user comparison |

## External Dependencies

- **Codeforces API** — `user.info`, `user.status`, `user.rating`, `problemset.problems`, `contest.standings`
- Rate limits apply; caching is critical for production use.

## Scalability Notes

Current design suits single-instance deployment. For scale:

1. Replace SQLite with PostgreSQL
2. Replace in-memory cache with Redis
3. Background job queue for initial submission fetch (large handles)
4. Normalize submissions into DB tables for SQL-based analytics
