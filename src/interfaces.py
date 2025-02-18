from abc import ABC, abstractmethod
from typing import List, Optional

class ContentGenerator(ABC):
    @abstractmethod
    def generate(self, requirements: str, word_count: int) -> str:
        pass

class ImageProcessor(ABC):
    @abstractmethod
    def generate(self, content: str, style: str, watermark: Optional[str] = None) -> List[str]:
        pass 