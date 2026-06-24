from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def get_health():
    return {"message":"Internal router is healthy"}
