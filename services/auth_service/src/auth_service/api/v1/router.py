from fastapi import APIRouter

from auth_service.config.settings import settings
from auth_service.api.v1.auth import router as auth_router

router = APIRouter()
# path: api/v1/auth

@router.get("/auth/health")
def health_check():
    return {
        "msg":"Auth service is healthy", 
        "app_name": settings.app_name, 
        "app_version": settings.app_version
        }

router.include_router(auth_router, prefix="/auth", tags=["auth"])
