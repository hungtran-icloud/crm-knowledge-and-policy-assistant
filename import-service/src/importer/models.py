"""
Data models and schemas for SongNhat CRM Knowledge and Policy Assistant
Implements: DAT 01 (Provenance), DAT 02 (Integrity), DAT 06 (Critical fields), DAT 07 (CRM context O1)
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List

class PolicyStatus(str, Enum):
    DRAFT = "draft"
    OWNER_REVIEWED = "owner_reviewed"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    EFFECTIVE = "effective"
    SUPERSEDED = "superseded"
    WITHDRAWN = "withdrawn"

class BatchType(str, Enum):
    SNAPSHOT = "snapshot"
    INCREMENT = "increment"

class ReconciliationStatus(str, Enum):
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"

class OperatorType(str, Enum):
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="
    BETWEEN = "between"
    IN = "in"

class FieldType(str, Enum):
    NUMBER = "number"
    CURRENCY = "currency"
    PERCENTAGE = "percentage"
    DURATION_DAYS = "duration_days"
    ROLE_NAME = "role_name"
    BOOLEAN = "boolean"
    STRING = "string"

@dataclass
class PassageRecord:
    document_id: str
    passage_id: str
    title: str
    original_reference: str
    language: str = "vi-VN"
    owner_role: str = ""
    approver_role: str = ""
    version: str = "1.0.0"
    recorded_at: str = ""
    effective_from: str = ""
    effective_to: Optional[str] = None
    status: PolicyStatus = PolicyStatus.DRAFT
    scope_branch: str = "ALL"
    scope_customer_tier: str = "ALL"
    scope_product_line: str = "ALL"
    superseded_by: Optional[str] = None
    content_text: str = ""
    has_footnotes_or_tables: bool = False
    footnotes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if isinstance(d["status"], PolicyStatus):
            d["status"] = d["status"].value
        return d

@dataclass
class CriticalFieldRecord:
    rule_id: str
    clause_ref: str
    field_name: str
    field_type: FieldType = FieldType.NUMBER
    operator: OperatorType = OperatorType.LE
    threshold_value: str = ""
    unit_or_currency: str = ""
    approval_role: str = ""
    exception_route: str = ""
    effective_from: str = ""
    effective_to: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if isinstance(d["field_type"], FieldType):
            d["field_type"] = d["field_type"].value
        if isinstance(d["operator"], OperatorType):
            d["operator"] = d["operator"].value
        return d

@dataclass
class CRMRecord:
    """Option O1 minimal CRM context record"""
    account_id: str
    record_key: str
    customer_tier: str
    industry: str
    assigned_sales_role: str
    credit_limit_vnd: float
    open_warranty_tickets: int
    account_status: str
    updated_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class QuarantineRecord:
    batch_id: str
    file_name: str
    row_number: int
    raw_data: str
    error_code: str
    error_reason: str
    quarantined_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class TombstoneRecord:
    entity_type: str  # 'passage' or 'critical_field' or 'crm_record'
    entity_id: str
    tombstone_at: str
    tombstone_by_role: str
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ManifestRecord:
    batch_id: str
    batch_type: BatchType
    schema_name: str
    file_name: str
    file_hash_sha256: str
    timestamp: str
    expected_rows: int
    accepted_rows: int
    quarantined_rows: int
    tombstone_rows: int
    reconciliation_status: ReconciliationStatus
    snapshot_age_iso: str
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if isinstance(d["batch_type"], BatchType):
            d["batch_type"] = d["batch_type"].value
        if isinstance(d["reconciliation_status"], ReconciliationStatus):
            d["reconciliation_status"] = d["reconciliation_status"].value
        return d

