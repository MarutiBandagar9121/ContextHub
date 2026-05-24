from fastapi import APIRouter

from auth_service.config.settings import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "msg":"Auth service is healthy", 
        "app_name": settings.app_name, 
        "app_version": settings.app_version
        }