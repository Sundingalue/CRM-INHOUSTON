from fastapi import APIRouter, Depends
from app.deps import get_current_user
router = APIRouter()

@router.get("/me")
def me(current=Depends(get_current_user)):
    return {"id": current.id, "email": current.email, "full_name": current.full_name, "role": current.role, "tenant_id": current.tenant_id}
