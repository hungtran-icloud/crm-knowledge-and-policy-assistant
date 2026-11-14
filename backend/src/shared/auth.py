"""
Shared auth dependencies — RBAC permission check.
Business rules: quyền truy cập phải được xác thực ở backend, không dựa vào prompt.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/identity/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: validate JWT, load user + roles from DB
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not implemented")


async def require_role(required_role: str):
    # TODO: check user role
    pass
