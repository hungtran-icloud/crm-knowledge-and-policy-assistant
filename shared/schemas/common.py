"""Common schemas shared across all services."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid


class BatchType(str, Enum):
    snapshot = "snapshot"
    increment = "increment"


class ReconciliationStatus(str, Enum):
    match = "MATCH"
    mismatch = "MISMATCH"


class HealthStatus(BaseModel):
    status: Literal["ok", "degraded", "down"]
    service: str
    version: str
    checks: Dict[str, bool]


class AuditEvent(BaseModel):
    """Audit event emitted by all services to audit-ops-service."""
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    service: str
    event_type: str  # e.g. batch_accepted, withdrawal_executed, answer_generated, permission_denied
    actor_id: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
