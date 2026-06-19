from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os

# Explicitly load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    cf_api_base: str = "https://codeforces.com/api"
    cors_origins: List[str] = ["*"]
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        extra = "ignore"

settings = Settings()
