from fastapi import FastAPI
from auth_service.config.settings import settings
from auth_service.api.v1.router import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")
