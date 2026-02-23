"""
metadata_extractor.py
Extracts basic metadata from an image file and generates a unique image_id.
Constructor: logger
"""

import hashlib
import os
from logging import Logger
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None


class MetadataExtractor:

    def __init__(self, logger: Logger):
        self.logger = logger

    def extract_metadata(self, image_path: str) -> dict:
        """
        Extract basic metadata from the image file.

        Returns:
            dict with keys: filename, file_size, width, height, format
        """
        path = Path(image_path)
        self.logger.info("Extracting metadata for: %s", path.name)

        metadata = {
            "filename": path.name,
            "file_size": os.path.getsize(image_path),
            "format": path.suffix.lstrip(".").upper(),
        }

        # dimensions from Pillow if available
        if Image is not None:
            try:
                with Image.open(image_path) as img:
                    metadata["width"], metadata["height"] = img.size
            except Exception as e:
                self.logger.warning("Could not read image dimensions: %s", e)
                metadata["width"] = None
                metadata["height"] = None
        else:
            metadata["width"] = None
            metadata["height"] = None

        self.logger.info("Metadata: %s", metadata)
        return metadata

    def generate_image_id(self, image_path: str) -> str:
        """
        Generate a unique image_id based on file content hash.

        Uses SHA-256 of the file bytes so the same image always gets the same ID.
        """
        self.logger.info("Generating image_id for: %s", Path(image_path).name)

        sha = hashlib.sha256()
        with open(image_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha.update(chunk)

        image_id = sha.hexdigest()[:16]
        self.logger.info("image_id: %s", image_id)
        return image_id
