from typing import List, Dict, Any
from app.adapters.base import OCRAdapter
from app.core.config import settings
from app.core.errors import ServiceUnavailableError


class PPStructureV3Adapter(OCRAdapter):
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        try:
            from paddleocr import PPStructure
        except Exception as e:
            raise ServiceUnavailableError(
                f"PPStructure import failed. Ensure PaddleOCR package support is installed. Details: {str(e)}"
            )

        try:
            self._client = PPStructure(
                show_log=False,
                use_gpu=settings.USE_GPU,
            )
            return self._client
        except Exception as e:
            raise ServiceUnavailableError(
                f"Failed to initialize PP-Structure. Check package version, model availability, and runtime setup. Details: {str(e)}"
            )

    def run(self, image_path: str) -> List[Dict[str, Any]]:
        client = self._get_client()

        try:
            result = client(image_path)
        except Exception as e:
            raise ServiceUnavailableError(
                f"PP-Structure inference failed. Details: {str(e)}"
            )

        parsed: List[Dict[str, Any]] = []

        for item in result or []:
            parsed.append(
                {
                    "text": item.get("res") if isinstance(item, dict) else None,
                    "score": None,
                    "bbox": item.get("bbox") if isinstance(item, dict) else None,
                    "type": item.get("type") if isinstance(item, dict) else "structure",
                    "raw": item,
                }
            )

        return parsed