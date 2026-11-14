"""
Module: feedback
Ghi nhận phản hồi và đề xuất chỉnh sửa tri thức
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "feedback", "status": "not-implemented"}
