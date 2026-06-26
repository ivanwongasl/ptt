from app.adapters.pp_ocr_adapter import PPOCRAdapter
from app.adapters.paddleocr_vl_adapter import PaddleOCRVLAdapter
from app.adapters.pp_structure_v3_adapter import PPStructureV3Adapter


class OCRService:
    def __init__(self):
        self.pp_ocr_adapter = PPOCRAdapter()
        self.paddleocr_vl_adapter = PaddleOCRVLAdapter()
        self.pp_structure_v3_adapter = PPStructureV3Adapter()


ocr_service = OCRService()