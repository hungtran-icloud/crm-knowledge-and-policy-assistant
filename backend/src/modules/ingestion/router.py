"""
Module: ingestion
Import CSV, validate, manifest, quarantine, reconciliation
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "ingestion", "status": "not-implemented"}
