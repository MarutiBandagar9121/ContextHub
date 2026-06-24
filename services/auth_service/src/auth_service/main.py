from contextlib import asynccontextmanager

from fastapi import FastAPI
from auth_service.config.settings import settings
from auth_service.api.v1.router import router
from auth_service.api_internal.v1.internal_router import router as internal_router

from auth_service.db.session import engine
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here (if needed)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise e
    yield
    # Shutdown code here (if needed)

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1", tags=["api", "v1"])
app.include_router(internal_router, prefic="/internal/api/v1", tags=["internal_api"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth_service.main:app", host="0.0.0.0", port=settings.port, reload=True)