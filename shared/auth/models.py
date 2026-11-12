"""
Auth placeholder models.
SEC01: Use organization-managed identities and least privilege.
This module is a stub — replace with actual org identity provider integration before G2.
"""
from enum import Enum
from pydantic import BaseModel
from typing import List


class UserRole(str, Enum):
    READER = "reader"
    POLICY_OWNER = "policy_owner"
    PUBLISHER = "publisher"
    STEWARD = "steward"
    ADMINISTRATOR = "administrator"


class AuthUser(BaseModel):
    """
    Stub authenticated user. In production, populate from verified JWT claims.
    SEC01: Enforce policy audience and CRM access before retrieval, generation and display.
    """
    user_id: str
    display_name: str
    roles: List[UserRole]
    policy_families: List[str] = []  # Authorized policy families for this user
    can_access_crm_context: bool = False  # Option O1 only, requires separate authorization
