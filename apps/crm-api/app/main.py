from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tenants, branding, me
from app.core.config import settings

app = FastAPI(title="CRM-INH API", version="0.2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True, "service": "crm-api"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(me.router, tags=["me"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(branding.router, prefix="/branding", tags=["branding"])
