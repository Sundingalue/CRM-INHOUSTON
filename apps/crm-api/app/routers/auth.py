from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models import Tenant, User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas import Token
from pydantic import BaseModel

router = APIRouter()
Base.metadata.create_all(bind=engine)

class RegisterIn(BaseModel):
    tenant_name: str
    tenant_slug: str
    email: str
    password: str
    full_name: str = ""

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=Token)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.slug == body.tenant_slug).first()
    if t:
        raise HTTPException(status_code=400, detail="Tenant slug already exists")
    t = Tenant(name=body.tenant_name, slug=body.tenant_slug)
    db.add(t); db.commit(); db.refresh(t)
    u = User(tenant_id=t.id, email=body.email, full_name=body.full_name, hashed_password=hash_password(body.password), role="owner")
    db.add(u); db.commit()
    token = create_access_token(sub=u.email, tid=u.tenant_id)
    return Token(access_token=token)

@router.post("/login", response_model=Token)
def login(body: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email).first()
    if not u or not verify_password(body.password, u.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=u.email, tid=u.tenant_id)
    return Token(access_token=token)
