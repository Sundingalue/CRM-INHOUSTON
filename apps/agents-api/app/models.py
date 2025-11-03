from sqlalchemy import Column, Integer, String, Text
from app.db import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True, nullable=False)
    name = Column(String(120), nullable=False)
    provider = Column(String(50), nullable=False)   # "openai" | "elevenlabs" | "gemini"
    model = Column(String(120), nullable=False)     # p.ej. "gpt-4o-mini"
    voice = Column(String(120), nullable=True)      # id de voz (si aplica)
    language = Column(String(20), nullable=True)    # "es", "en", etc.
    phone_number = Column(String(32), nullable=True)# número asignado (si aplica)
    config_json = Column(Text, nullable=True)       # JSON como string (prompt, temp, etc.)
