from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Ingestion api",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api",
    tags=["Ingestion"]
)


@app.get("/")
def root():
    return {"message": "Ingestion api is running"}