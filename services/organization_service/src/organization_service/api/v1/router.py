from fastapi import APIRouter

from organization_service.api.v1.organization_routes import router as organization_routes
from organization_service.config.settings import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "msg":"Auth service is healthy", 
        "app_name": settings.app_name, 
        "app_version": settings.app_version
        }

router.include_router(organization_routes, prefix="/organization", tags=["organization"])