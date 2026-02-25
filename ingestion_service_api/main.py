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

from ingestion_config import IngestionConfig
from OCRengine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_client import MongoLoaderClient
from kafka_publisher import KafkaPublisher
from ingestion_orchestrator import IngestionOrchestrator
import routes

# ---- logger (single logger, passed to all components) ----
logger = get_logger("ingestion-service")

# ---- build components (dependency injection) ----
config = IngestionConfig()
ocr_engine = OCREngine(logger)
metadata_extractor = MetadataExtractor(logger)
gridfs_client = MongoLoaderClient(config.gridfs_service_url, logger)
kafka_publisher = KafkaPublisher(config.bootstrap_servers, config.kafka_topic_raw, logger)

# ----orchestrator ----
orchestrator = IngestionOrchestrator(
    config=config,
    ocr_engine=ocr_engine,
    metadata=metadata_extractor,
    Gridfs=gridfs_client,
    publisher=kafka_publisher,
    logger=logger,
)

# ---- FastAPI ----
app = FastAPI(title="Ingestion Service")
app.include_router(routes.router)
logger.info("Ingestion Service is ready")


