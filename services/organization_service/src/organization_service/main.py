from contextlib import contextmanager

from fastapi import FastAPI
from sqlalchemy import text

from organization_service.db.session import engine
from organization_service.api.v1.router import router as api_v1_router

@contextmanager
async def lifespan(app = FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text("Select 1"))
    except Exception as e:
        print("Database Connection failed")
        raise e
    yield
    # shutdown logic
    
app = FastAPI(lifespan = lifespan)

app.include_router(api_v1_router, prefix="/api/v1", tags=["api", "v1"])
