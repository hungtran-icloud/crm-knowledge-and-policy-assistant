"""
CRM Context schema — Option O1 only.
Minimal approved fields per DAT07 and SEC02.
Only use after separate need, permission, and lawful processing decision.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class CRMContextBase(BaseModel):
    account_id: str
    record_key: str
    customer_tier: str
    industry: str
    assigned_sales_role: str
    credit_limit_vnd: float
    open_warranty_tickets: int
    account_status: str
    updated_at: datetime


class CRMContextCreate(CRMContextBase):
    pass


class CRMContextRead(CRMContextBase):
    id: uuid.UUID
