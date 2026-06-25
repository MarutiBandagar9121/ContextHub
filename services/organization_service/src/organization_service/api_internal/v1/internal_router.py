from fastapi import APIRouter

from organization_service.api_internal.v1.user_routes import router as user_router

router = APIRouter()

router.include_router(user_router)
