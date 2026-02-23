"""
OCRengine.py
Extracts text from an image using pytesseract.
Constructor: logger
"""

from logging import Logger
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
except ImportError:
    pytesseract = None
    Image = None


class OCREngine:

    def __init__(self, logger: Logger):
        self.logger = logger

    def extract_text(self, image_path: str) -> str:
        """
        Run OCR on the given image file.

        Args:
            image_path: Path to the image file.

        Returns:
            raw_text extracted from the image.
        """
        self.logger.info("Running OCR on: %s", Path(image_path).name)

        if pytesseract is None or Image is None:
            self.logger.error("pytesseract or Pillow not installed")
            raise ImportError("pip install pytesseract Pillow")

        try:
            img = Image.open(image_path)
            raw_text = pytesseract.image_to_string(img)
            self.logger.info(
                "OCR complete for %s — extracted %d characters",
                Path(image_path).name,
                len(raw_text),
            )
            return raw_text

        except Exception as e:
            self.logger.error("OCR failed for %s: %s", image_path, e)
            raise
