"""
Module: identity
Đăng nhập, xác thực, phân quyền RBAC
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"module": "identity", "status": "not-implemented"}
