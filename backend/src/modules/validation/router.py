"""
Module: validation
Kiểm tra citation, critical fields, tính đầy đủ của câu trả lời
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "validation", "status": "not-implemented"}
