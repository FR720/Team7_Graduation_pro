import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str

    # JWT Configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Server Configuration
    API_V1_PREFIX: str
    BACKEND_CORS_ORIGINS: List[str]

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"

settings = Settings()