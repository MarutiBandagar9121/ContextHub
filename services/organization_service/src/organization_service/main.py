from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from organization_service.config.settings import settings
from organization_service.db.session import engine
from organization_service.api.v1.router import router as api_v1_router
from organization_service.api_internal.v1.internal_router import router as api_internal_v1_router

@asynccontextmanager
async def lifespan(app = FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text("Select 1"))
    except Exception as e:
        print("Database Connection failed")
        raise e
    yield
    # shutdown logic
    
app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix="/api/v1", tags=["api_v1"])
app.include_router(api_internal_v1_router, prefix="/internal/v1", tags=["internal_api_v1"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("organization_service.main:app", host="0.0.0.0", port=settings.port, reload=True)
