from fastapi import APIRouter

from organization_service.api_internal.v1.internal_router import router as internal_router

router = APIRouter()

router.include_router(internal_router)
