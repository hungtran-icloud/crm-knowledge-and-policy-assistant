"""
Module: admin
Quản trị người dùng, cấu hình hệ thống, quyền vận hành
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "admin", "status": "not-implemented"}
