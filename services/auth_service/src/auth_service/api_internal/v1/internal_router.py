from fastapi import APIRouter

from auth_service.api_internal.v1.user_internal_routes import router as user_internal_rouets

router = APIRouter()

router.include_router(user_internal_rouets, prefix="/user")