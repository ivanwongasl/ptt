from typing import List, Dict, Any
from app.adapters.base import OCRAdapter
from app.core.config import settings
from app.core.errors import ServiceUnavailableError


class PPOCRAdapter(OCRAdapter):
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        try:
            from paddleocr import PaddleOCR
        except Exception as e:
            raise ServiceUnavailableError(
                f"PaddleOCR import failed. Ensure dependencies are installed correctly. Details: {str(e)}"
            )

        try:
            self._client = PaddleOCR(
                use_angle_cls=settings.OCR_USE_ANGLE_CLS,
                lang=settings.OCR_LANG,
            )
            return self._client
        except Exception as e:
            raise ServiceUnavailableError(
                f"Failed to initialize PP-OCR. Check Paddle runtime, model download, and package compatibility. Details: {str(e)}"
            )

    def run(self, image_path: str) -> List[Dict[str, Any]]:
        client = self._get_client()

        try:
            result = client.ocr(image_path, cls=settings.OCR_USE_ANGLE_CLS)
        except Exception as e:
            raise ServiceUnavailableError(
                f"PP-OCR inference failed. Details: {str(e)}"
            )

        parsed: List[Dict[str, Any]] = []

        for page in result or []:
            for line in page or []:
                try:
                    parsed.append(
                        {
                            "text": line[1][0],
                            "score": float(line[1][1]),
                            "bbox": line[0],
                            "type": "text",
                            "raw": line,
                        }
                    )
                except Exception:
                    parsed.append(
                        {
                            "text": None,
                            "score": None,
                            "bbox": None,
                            "type": "unknown",
                            "raw": line,
                        }
                    )

        return parsed