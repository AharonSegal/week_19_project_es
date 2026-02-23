"""
ingestion orchestrator
1- scans the image folder 
2- sends images to OCRengine.py -> extract text from image
3- sends to metadata_extractor.py -> extract metadata
4- sends to mongo_client.py -> to send to loader 
5- sends to kafka_publisher.py
"""