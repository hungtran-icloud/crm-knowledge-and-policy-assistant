"""
Module: retrieval
Tìm kiếm ngữ nghĩa (pgvector), từ khóa, lọc bằng chứng
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "retrieval", "status": "not-implemented"}
