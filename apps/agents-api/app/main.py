from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core_config import settings
from app.db import Base, engine
from app.routers import agents  # si ya existe tu router (no pasa nada si está vacío)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas del API (agentes, etc.)
app.include_router(agents.router)

@app.get("/health")
def health():
    return {"status": "ok"}

# UI estática (mini-CRM) en /app
app.mount("/app", StaticFiles(directory="app/web", html=True), name="web")
