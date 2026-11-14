"""
Module: policy
Phiên bản, thẩm quyền, trạng thái xuất bản, effective dates, phạm vi
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "policy", "status": "not-implemented"}
