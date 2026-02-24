"""
main.py
Ingestion Service entry point.
Creates logger, wires all dependencies, starts FastAPI.
"""
# for local run 
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import FastAPI

from shared.logger import get_logger

from ingestion_service_api.ingestion_config import IngestionConfig
from OCRengine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_client import MongoLoaderClient
from kafka_publisher import KafkaPublisher
from ingestion_orchestrator import IngestionOrchestrator
from routes import router

# ---- logger (single logger, passed to all components) ----
logger = get_logger("ingestion-service")

# ---- FastAPI ----
app = FastAPI(title="Ingestion Service")
app.include_router(router)
logger.info("Ingestion Service is ready")
