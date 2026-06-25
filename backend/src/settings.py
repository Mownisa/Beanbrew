from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_CONN_STRING: str
    GEMINI_API_KEY: str
    MCP_SERVER_URL: str = "http://localhost:8001/mcp"
    SECRET_KEY: str = "change-me-in-production"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


config = get_settings()
