from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Tenant
from app.schemas import BrandingOut
from app.deps import get_current_user

router = APIRouter()

@router.get("", response_model=BrandingOut)
def get_branding(current=Depends(get_current_user), db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.id == current.tenant_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return BrandingOut(logo_url=t.logo_url, color_primary=t.color_primary, color_accent=t.color_accent, name=t.name)
