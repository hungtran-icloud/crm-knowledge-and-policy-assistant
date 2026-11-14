"""
Module: answer
Điều phối RAG: applicability → retrieval → LLM generation → validation
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "answer", "status": "not-implemented"}
