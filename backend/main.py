import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routers import analysis, api, users

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Codeforces Contest Analyzer API",
    description="Analytics, recommendations, and contest performance insights for Codeforces users",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(analysis.router)
app.include_router(api.router)


@app.get("/")
def read_root():
    return {
        "message": "Codeforces Contest Analyzer API",
        "version": "2.0.0",
        "docs": "/docs",
    }
