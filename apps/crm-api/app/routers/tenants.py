from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Tenant
from app.schemas import TenantIn, TenantOut
from app.deps import get_current_user

router = APIRouter()

@router.get("", response_model=list[TenantOut])
def list_tenants(current=Depends(get_current_user), db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.id == current.tenant_id).first()
    return [TenantOut(id=t.id, name=t.name, slug=t.slug, color_primary=t.color_primary, color_accent=t.color_accent, logo_url=t.logo_url)]

@router.put("/{tenant_id}", response_model=TenantOut)
def update_tenant(tenant_id: int, body: TenantIn, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current.tenant_id != tenant_id and current.role != "owner":
        raise HTTPException(status_code=403, detail="Forbidden")
    t = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    t.name = body.name; t.slug = body.slug; t.color_primary = body.color_primary; t.color_accent = body.color_accent; t.logo_url = body.logo_url
    db.commit(); db.refresh(t)
    return TenantOut(id=t.id, name=t.name, slug=t.slug, color_primary=t.color_primary, color_accent=t.color_accent, logo_url=t.logo_url)
