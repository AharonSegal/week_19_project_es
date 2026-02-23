import json
from fastapi import APIRouter
from dotenv import dotenv_values


config = dotenv_values(".env")


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/alerts-by-border-and-priority")
def first():
    pass