from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core_config import settings
from app.db import Base, engine
from app.routers import agents

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(agents.router)

@app.get("/health")
def health():
    return {"status": "ok"}
