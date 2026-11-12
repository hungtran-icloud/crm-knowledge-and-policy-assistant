"""Passage schemas for the SongNhat CRM Knowledge & Policy Assistant."""
from enum import Enum
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import uuid


class PassageStatus(str, Enum):
    draft = "draft"
    owner_reviewed = "owner_reviewed"
    approved = "approved"
    scheduled = "scheduled"
    effective = "effective"
    superseded = "superseded"
    withdrawn = "withdrawn"


class PassageBase(BaseModel):
    document_id: str
    passage_id: str
    title: str
    original_reference: str
    language: str = "vi-VN"
    owner_role: str = ""
    approver_role: str = ""
    version: str = "1.0.0"
    recorded_at: Optional[datetime] = None
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None
    status: PassageStatus = PassageStatus.draft
    scope_branch: str = "ALL"
    scope_customer_tier: str = "ALL"
    scope_product_line: str = "ALL"
    superseded_by: Optional[str] = None
    content_text: str = ""
    has_footnotes_or_tables: bool = False
    footnotes: Optional[str] = None

    @field_validator("content_text")
    @classmethod
    def content_text_max_length(cls, v: str) -> str:
        """DAT08: At most 6,000 Unicode characters per imported text item."""
        if len(v) > 6000:
            raise ValueError(
                "content_text must be at most 6,000 Unicode characters (DAT08)"
            )
        return v


class PassageCreate(PassageBase):
    """Schema for write operations."""
    pass


class PassageRead(PassageBase):
    """Schema for read operations — includes server-assigned fields."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
