from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base
from routers import users, analysis

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Competitive Programming Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(analysis.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Competitive Programming Analyzer API"}
