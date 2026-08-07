import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinPilot AI - Enterprise Financial Operations Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Auth & JWT
    SECRET_KEY: str = "finpilot-enterprise-super-secret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "sqlite:///./finpilot.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./finpilot.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # Groq LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.1
    GROQ_MAX_TOKENS: int = 4096

    # RAG & ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Financial Compliance & Policy Controls
    AUTO_APPROVAL_THRESHOLD_INR: float = 25000.0
    PII_REDACTION_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
