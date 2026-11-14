"""
Module: knowledge
Quản lý tài liệu, phiên bản, passage, metadata
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "knowledge", "status": "not-implemented"}
