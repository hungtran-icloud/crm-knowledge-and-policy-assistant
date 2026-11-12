"""Critical field schemas for the SongNhat CRM Knowledge & Policy Assistant."""
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class FieldType(str, Enum):
    number = "number"
    currency = "currency"
    percentage = "percentage"
    duration_days = "duration_days"
    role_name = "role_name"
    boolean = "boolean"
    string = "string"


class OperatorType(str, Enum):
    lt = "lt"
    le = "le"
    gt = "gt"
    ge = "ge"
    eq = "eq"
    between = "between"
    in_list = "in_list"


class CriticalFieldBase(BaseModel):
    rule_id: str
    clause_ref: str
    field_name: str
    field_type: FieldType = FieldType.number
    operator: OperatorType = OperatorType.le
    threshold_value: str = ""
    unit_or_currency: str = ""
    approval_role: str = ""
    exception_route: str = ""
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None


class CriticalFieldCreate(CriticalFieldBase):
    """Schema for write operations."""
    pass


class CriticalFieldRead(CriticalFieldBase):
    """Schema for read operations — includes server-assigned fields."""
    id: uuid.UUID
    created_at: datetime
