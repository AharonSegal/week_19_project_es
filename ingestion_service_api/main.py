"""
main.py
Ingestion Service entry point.
Creates logger, wires all dependencies, starts FastAPI.
"""

from fastapi import FastAPI

from shared.logger import get_logger

from ingestionConfig import IngestionConfig
from OCRengine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_client import MongoLoaderClient
from kafka_publisher import KafkaPublisher
from ingestion_orchestrator import IngestionOrchestrator
from routes import router, init_routes

# ---- logger (single logger, passed to all components) ----
logger = get_logger("ingestion-service")

# ---- config ----
config = IngestionConfig()
config.validate()
logger.info("Config loaded: image_dir=%s, topic=%s", config.image_directory, config.kafka_topic_raw)

# ---- components (dependency injection via constructor) ----
ocr_engine = OCREngine(logger=logger)
metadata_extractor = MetadataExtractor(logger=logger)

mongo_client = MongoLoaderClient(
    gridfs_service_url=config.gridfs_service_url,
    logger=logger,
)

publisher = KafkaPublisher(
    bootstrap_servers=config.bootstrap_servers,
    topic_name=config.kafka_topic_raw,
    logger=logger,
)

orchestrator = IngestionOrchestrator(
    config=config,
    ocr_engine=ocr_engine,
    metadata_extractor=metadata_extractor,
    mongo_client=mongo_client,
    publisher=publisher,
    logger=logger,
)

# ---- FastAPI ----
app = FastAPI(title="Ingestion Service")
init_routes(orchestrator)
app.include_router(router)

logger.info("Ingestion Service is ready")
