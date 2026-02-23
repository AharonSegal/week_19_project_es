"""
routes.py
FastAPI routes for the Ingestion Service.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from ingestion_orchestrator import IngestionOrchestrator

router = APIRouter()

# will be set from main.py
orchestrator: IngestionOrchestrator = None


def init_routes(orch: IngestionOrchestrator):
    global orchestrator
    orchestrator = orch


@router.post("/ingest")
def ingest_all():
    """Scan the image directory and process all images."""
    if orchestrator is None:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    summary = orchestrator.run()
    return {"status": "ok", "summary": summary}


@router.post("/ingest/single")
async def ingest_single(file: UploadFile = File(...)):
    """
    Upload and process a single image.
    Saves to IMAGE_DIRECTORY then processes it.
    """
    if orchestrator is None:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    import os
    from pathlib import Path

    image_dir = orchestrator.config.image_directory
    file_path = os.path.join(image_dir, file.filename)

    # save uploaded file
    content = await file.read()
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)

    # process it
    orchestrator.process_image(file_path)

    return {"status": "ok", "filename": file.filename}


@router.get("/health")
def health():
    return {"status": "healthy", "service": "ingestion-service"}
