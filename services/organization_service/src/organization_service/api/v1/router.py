from fastapi import APIRouter
from organization_service.api.v1.organization_routes import router as organization_routes

router = APIRouter()

@router.get("/organization/health")
def get_hello():
    return {"msg":"Organization service is healthy"}

router.include_router(organization_routes, prefix="/organization", tags=["organization"])