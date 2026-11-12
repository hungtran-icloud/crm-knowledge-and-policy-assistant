"""
FastAPI dependency stubs for authentication and authorization.
Replace with real identity provider integration before G2 (legal review required per SEC03).
"""
from fastapi import Header, HTTPException
from typing import Optional
from shared.auth.models import AuthUser, UserRole


async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    x_user_roles: Optional[str] = Header(None),
) -> AuthUser:
    """
    STUB: Extract user from request headers.
    In production: validate JWT from org identity provider (SEC01).
    """
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    roles = []
    if x_user_roles:
        for r in x_user_roles.split(","):
            try:
                roles.append(UserRole(r.strip()))
            except ValueError:
                pass
    return AuthUser(user_id=x_user_id, display_name=x_user_id, roles=roles)


async def require_reader(user: AuthUser = None) -> AuthUser:
    """Require at minimum READER role."""
    if not user or not user.roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return user
