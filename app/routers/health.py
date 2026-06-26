from fastapi import APIRouter
from app.schemas.responses import HealthResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")