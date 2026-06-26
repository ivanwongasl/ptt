from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.ocr import router as ocr_router

app = FastAPI(
    title="OCR API Server",
    description="FastAPI server for PP-OCR, PaddleOCR-VL, PP-StructureV3, and health check",
    version="1.0.0",
)

app.include_router(health_router, tags=["health"])
app.include_router(ocr_router, prefix="/ocr", tags=["ocr"])