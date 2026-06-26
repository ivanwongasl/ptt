from abc import ABC, abstractmethod
from typing import List, Dict, Any


class OCRAdapter(ABC):
    @abstractmethod
    def run(self, image_path: str) -> List[Dict[str, Any]]:
        raise NotImplementedError