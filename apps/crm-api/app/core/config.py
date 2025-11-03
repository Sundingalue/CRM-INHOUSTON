# apps/crm-api/app/core/config.py
import os

class Settings:
    # Lee las variables de entorno sin usar Pydantic (evita el error de BaseSettings)
    SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
    JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "120"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm.db")

settings = Settings()
