from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    role: str
    tenant_id: int

class TenantIn(BaseModel):
    name: str
    slug: str
    color_primary: str = "#ffcc00"
    color_accent: str = "#000000"
    logo_url: Optional[str] = None

class TenantOut(TenantIn):
    id: int

class BrandingOut(BaseModel):
    logo_url: Optional[str] = None
    color_primary: str
    color_accent: str
    name: str
