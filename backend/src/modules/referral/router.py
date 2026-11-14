"""
Module: referral
Ghi nhận câu hỏi thiếu dữ kiện, chuyển Policy Owner
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "referral", "status": "not-implemented"}
