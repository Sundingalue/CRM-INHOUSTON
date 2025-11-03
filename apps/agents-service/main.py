# Agents service — IA Voz y Texto (CRUD + llamadas salientes/entrantes) con JWT
import os
from datetime import datetime
from typing import Optional, Dict, List, Literal

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from jose import jwt, JWTError

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agents.db")
ALLOWED_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
engine = create_engine(DATABASE_URL, connect_args={} if not DATABASE_URL.startswith("sqlite") else {"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

app = FastAPI(title="INH Agents Service", version="0.2.1")
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class AgentDB(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    tenant = Column(String(120), index=True, default="default")
    name = Column(String(120), nullable=False)
    provider = Column(String(30), nullable=False, default="elevenlabs")
    model = Column(String(120), nullable=True)
    voice_id = Column(String(120), nullable=True)
    language = Column(String(10), nullable=True, default="es")
    prompt = Column(Text, nullable=True)
    caller_id = Column(String(30), nullable=True)
    provider_phone = Column(String(30), nullable=True)
    temperature = Column(String(10), nullable=True, default="0.7")
    provider_meta = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class AgentIn(BaseModel):
    tenant: str = Field(default="")
    name: str
    provider: Literal["elevenlabs", "openai", "gemini"] = "elevenlabs"
    model: Optional[str] = None
    voice_id: Optional[str] = None
    language: Optional[str] = "es"
    prompt: Optional[str] = None
    caller_id: Optional[str] = None
    provider_phone: Optional[str] = None
    temperature: Optional[str] = "0.7"
    provider_meta: Optional[Dict] = None
    enabled: bool = True

class AgentOut(AgentIn):
    id: int
    created_at: datetime
    updated_at: datetime

class OutboundCallIn(BaseModel):
    to_number: str = Field(..., description="E.164 +1...")
    vars: Optional[Dict] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def claims_from_auth(authorization: str | None):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health():
    return {"ok": True, "service": "agents-service"}

@app.post("/agents", response_model=AgentOut)
def create_agent(body: AgentIn, authorization: str = Header(None), db: Session = Depends(get_db)):
    c = claims_from_auth(authorization)
    tid = c.get("tid")
    payload = body.dict()
    if not payload.get("tenant") and tid is not None:
        payload["tenant"] = str(tid)
    a = AgentDB(**payload)
    db.add(a); db.commit(); db.refresh(a)
    return AgentOut(**to_out(a))

@app.get("/agents", response_model=List[AgentOut])
def list_agents(tenant: Optional[str] = None, authorization: str = Header(None), db: Session = Depends(get_db)):
    c = claims_from_auth(authorization)
    default_tenant = str(c.get("tid")) if c.get("tid") is not None else None
    if tenant is None and default_tenant:
        tenant = default_tenant
    q = db.query(AgentDB)
    if tenant:
        q = q.filter(AgentDB.tenant == tenant)
    res = q.order_by(AgentDB.created_at.desc()).all()
    return [AgentOut(**to_out(a)) for a in res]

@app.get("/agents/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, authorization: str = Header(None), db: Session = Depends(get_db)):
    claims_from_auth(authorization)
    a = db.query(AgentDB).get(agent_id)
    if not a:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return AgentOut(**to_out(a))

@app.put("/agents/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: int, body: AgentIn, authorization: str = Header(None), db: Session = Depends(get_db)):
    claims_from_auth(authorization)
    a = db.query(AgentDB).get(agent_id)
    if not a:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    for k, v in body.dict().items():
        setattr(a, k, v)
    a.updated_at = datetime.utcnow()
    db.commit(); db.refresh(a)
    return AgentOut(**to_out(a))

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, authorization: str = Header(None), db: Session = Depends(get_db)):
    claims_from_auth(authorization)
    a = db.query(AgentDB).get(agent_id)
    if not a:
        raise HTTPException(statusCode=404, detail="Agente no encontrado")
    db.delete(a); db.commit()
    return {"ok": True, "deleted": agent_id}

@app.post("/agents/{agent_id}/outbound_call")
def outbound_call(agent_id: int, body: OutboundCallIn, authorization: str = Header(None), db: Session = Depends(get_db)):
    claims_from_auth(authorization)
    a = db.query(AgentDB).get(agent_id)
    if not a or not a.enabled:
        raise HTTPException(status_code=404, detail="Agente no disponible")
    # Aquí conectarías SDK del proveedor (queued para demo)
    result = {"status": "queued", "provider": a.provider, "to": body.to_number}
    return {"ok": True, "agent_id": agent_id, "result": result}

@app.post("/twilio/voice/inbound")
async def twilio_inbound(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    called = (form.get("To") or form.get("Called") or "").strip()
    if not called:
        return Response(content="<Response><Say language='es-MX'>No se recibió destino.</Say></Response>", media_type="application/xml")

    a = db.query(AgentDB).filter(AgentDB.enabled == True).filter((AgentDB.provider_phone == called) | (AgentDB.caller_id == called)).order_by(AgentDB.updated_at.desc()).first()
    if not a:
        return Response(content="<Response><Say language='es-MX'>No hay agente asignado a este número.</Say></Response>", media_type="application/xml")

    if a.provider_phone:
        t = f"""<Response><Dial callerId="{a.caller_id or ''}"><Number>{a.provider_phone}</Number></Dial></Response>"""
        return Response(content=t, media_type="application/xml")

    return Response(content="<Response><Say language='es-MX'>Gracias por llamar. En breve te atenderá un agente virtual.</Say></Response>", media_type="application/xml")

def to_out(a: AgentDB) -> Dict:
    import json
    meta = a.provider_meta
    if isinstance(meta, str):
        try:
            meta = json.loads(meta)
        except Exception:
            meta = {}
    return {
        "id": a.id, "tenant": a.tenant, "name": a.name, "provider": a.provider, "model": a.model,
        "voice_id": a.voice_id, "language": a.language, "prompt": a.prompt,
        "caller_id": a.caller_id, "provider_phone": a.provider_phone, "temperature": a.temperature,
        "provider_meta": meta or {}, "enabled": a.enabled, "created_at": a.created_at, "updated_at": a.updated_at,
    }
