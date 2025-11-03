from pydantic import BaseModel, Field
from typing import Optional

class AgentCreate(BaseModel):
    tenant_id: int
    name: str = Field(..., max_length=120)
    provider: str                  # "openai" | "elevenlabs" | "gemini"
    model: str                     # p.ej. "gpt-4o-mini"
    voice: Optional[str] = None
    language: Optional[str] = "es"
    phone_number: Optional[str] = None
    config_json: Optional[str] = None  # JSON como string (prompt, temperatura, etc.)

class AgentOut(BaseModel):
    id: int
    tenant_id: int
    name: str
    provider: str
    model: str
    voice: Optional[str]
    language: Optional[str]
    phone_number: Optional[str]
    config_json: Optional[str]

    class Config:
        from_attributes = True
