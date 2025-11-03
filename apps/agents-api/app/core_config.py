from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AGENTS API"
    # Usaremos la misma DB de Render (Postgres) o SQLite en local.
    DATABASE_URL: str = "sqlite:///./agents.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
