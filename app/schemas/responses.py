from typing import Any, List, Optional
from pydantic import BaseModel


class OCRItem(BaseModel):
    text: Optional[str] = None
    score: Optional[float] = None
    bbox: Optional[Any] = None
    type: Optional[str] = None
    raw: Optional[Any] = None


class OCRResponse(BaseModel):
    engine: str
    success: bool
    results: List[OCRItem]
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str