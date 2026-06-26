from typing import List, Dict, Any
from app.adapters.base import OCRAdapter
from app.core.errors import ServiceUnavailableError


class PaddleOCRVLAdapter(OCRAdapter):
    def run(self, image_path: str) -> List[Dict[str, Any]]:
        raise ServiceUnavailableError(
            "PaddleOCR-VL adapter is not implemented in this starter project. "
            "Keep the API contract stable and replace this adapter with your actual PaddleOCR-VL runtime integration, "
            "including required package version, model weights, and environment setup."
        )