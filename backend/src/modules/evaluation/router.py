"""
Module: evaluation
Quản lý bộ test, đo chất lượng retrieval/answer
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "evaluation", "status": "not-implemented"}
