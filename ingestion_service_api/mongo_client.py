"""
mongo_client.py
Sends the binary file to the GridFS Service via HTTP POST.
Constructor: gridfs_service_url, logger
"""

from logging import Logger
from pathlib import Path

import requests


class MongoLoaderClient:

    def __init__(self, gridfs_service_url: str, logger: Logger):
        self.gridfs_service_url = gridfs_service_url.rstrip("/")
        self.logger = logger

    def send(self, file_path: str, image_id: str) -> dict:
        """
        POST the binary file to the GridFS service.

        Args:
            file_path: Path to the image file.
            image_id:  Unique identifier for the image.

        Returns:
            Response JSON from the GridFS service.
        """
        filename = Path(file_path).name
        url = f"{self.gridfs_service_url}/upload"

        self.logger.info(
            "Sending file %s (image_id=%s) to GridFS at %s",
            filename, image_id, url,
        )

        try:
            with open(file_path, "rb") as f:
                files = {"file": (filename, f)}
                data = {"image_id": image_id}
                response = requests.post(url, files=files, data=data, timeout=30)

            response.raise_for_status()
            result = response.json()
            self.logger.info("GridFS upload success for image_id=%s", image_id)
            return result

        except requests.RequestException as e:
            self.logger.error(
                "GridFS upload failed for image_id=%s: %s", image_id, e
            )
            raise
