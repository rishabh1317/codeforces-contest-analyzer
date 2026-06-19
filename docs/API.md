# API Reference

Base URL: `http://localhost:8000`

Interactive docs: `/docs` (Swagger UI)

## Dashboard (Recommended)

### `GET /api/users/{handle}/dashboard`

Returns the complete analytics payload in one request.

**Response highlights:**
- `analysis` — weak/strong topics, tag recommendations
- `tag_analysis` — all tags for heatmap
- `percentile` — last 10 contest percentiles
- `contest_analytics` — rating timeline, consistency, upsolves
- `problem_recommendations` — scored problems with reasons
- `rating_prediction` — forecast range and confidence

## Topic Analysis

### `GET /api/users/{handle}/tag-analysis`

```json
[
  {
    "tag": "dp",
    "total": 45,
    "solved": 20,
    "ac_rate": 0.44,
    "avg_difficulty": 1350
  }
]
```

## Contest Analytics

### `GET /api/users/{handle}/contest-analytics`

Returns `total_contests`, `rating_timeline`, `rank_timeline`, `consistency_score`, `upsolve_count`, `summary`, etc.

## Recommendations

### `GET /api/users/{handle}/recommendations?limit=10`

Query params: `limit` (1–25, default 10)

```json
[
  {
    "contest_id": 1900,
    "index": "A",
    "name": "Problem Name",
    "rating": 1200,
    "tags": ["dp"],
    "url": "https://codeforces.com/problemset/problem/1900/A",
    "reason": "Weak area: dp; Difficulty matches your level",
    "difficulty_progression": "comfortable"
  }
]
```

## Rating Prediction

### `GET /api/users/{handle}/rating-prediction`

```json
{
  "current_rating": 1500,
  "predicted_rating_low": 1480,
  "predicted_rating_high": 1580,
  "predicted_rating_mid": 1530,
  "confidence_score": 0.72,
  "trend": "growing",
  "suggested_improvements": ["..."]
}
```

## Compare

### `GET /api/compare?handle1={h1}&handle2={h2}`

Returns `rival1`, `rival2` stats plus `insights` array.

## Legacy

### `GET /analysis/codeforces/{handle}`

Backward-compatible analysis response with `weak_topics`, `strongest_topics`, `recommendations`.

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Invalid platform or parameters |
| 404 | User not found on Codeforces |
| 502 | Codeforces API error |
| 503 | Codeforces API unavailable |
