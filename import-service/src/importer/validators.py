"""
Validators for CSV schemas: passages.csv, critical_fields.csv, and crm_context.csv (O1)
Implements: DAT 01, DAT 02, DAT 06, DAT 07, DAT 08, VN 01, VN 03
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from src.importer.models import (
    PassageRecord, CriticalFieldRecord, CRMRecord, QuarantineRecord,
    PolicyStatus, OperatorType, FieldType
)

ISO8601_PATTERN = re.compile(
    r'^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?$'
)

class ValidationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

def parse_iso8601(val: str, field_name: str) -> str:
    if not val or not val.strip():
        return ""
    val_clean = val.strip()
    if not ISO8601_PATTERN.match(val_clean):
        raise ValidationError("ERR_INVALID_DATE_FORMAT", f"{field_name} must be in ISO 8601 format, got: '{val}'")
    return val_clean

class PassageValidator:
    """Validator for passages.csv (Approved knowledge corpus)"""
    REQUIRED_COLUMNS = [
        "document_id", "passage_id", "title", "original_reference",
        "language", "owner_role", "approver_role", "version",
        "recorded_at", "effective_from", "effective_to", "status",
        "scope_branch", "scope_customer_tier", "scope_product_line",
        "superseded_by", "content_text", "has_footnotes_or_tables", "footnotes"
    ]
    MAX_CONTENT_CHARS = 6000  # RFP Section 2 / DAT 08: At most 6,000 Unicode characters per imported item

    @classmethod
    def validate_row(cls, row: Dict[str, str], row_num: int) -> Tuple[Optional[PassageRecord], Optional[ValidationError]]:
        try:
            # Check mandatory key fields
            for mandatory in ["document_id", "passage_id", "title", "content_text", "owner_role", "approver_role", "version"]:
                if not row.get(mandatory) or not str(row[mandatory]).strip():
                    raise ValidationError("ERR_MISSING_MANDATORY_FIELD", f"Field '{mandatory}' cannot be empty")

            # Check character cap (no silent truncation - DAT 08)
            content = str(row["content_text"]).strip()
            if len(content) > cls.MAX_CONTENT_CHARS:
                raise ValidationError(
                    "ERR_CONTENT_TOO_LONG",
                    f"Content has {len(content)} characters, exceeding maximum limit of {cls.MAX_CONTENT_CHARS}"
                )

            # Language check (VN 01)
            lang = row.get("language", "vi-VN").strip()
            if lang != "vi-VN":
                raise ValidationError("ERR_INVALID_LANGUAGE", f"Only 'vi-VN' is supported for base scope, got: '{lang}'")

            # Status enum check
            status_raw = row.get("status", "draft").strip().lower()
            try:
                status = PolicyStatus(status_raw)
            except ValueError:
                valid_statuses = [s.value for s in PolicyStatus]
                raise ValidationError(
                    "ERR_INVALID_STATUS",
                    f"Status '{status_raw}' invalid. Must be one of {valid_statuses}"
                )

            # Dates validation
            recorded_at = parse_iso8601(row.get("recorded_at", ""), "recorded_at")
            effective_from = parse_iso8601(row.get("effective_from", ""), "effective_from")
            effective_to = parse_iso8601(row.get("effective_to", ""), "effective_to") or None

            # Footnote & Table completeness (DAT 08)
            has_footnotes_raw = str(row.get("has_footnotes_or_tables", "false")).strip().lower()
            has_footnotes = has_footnotes_raw in ["true", "1", "yes"]
            footnotes = row.get("footnotes", "").strip() or None
            if has_footnotes and not footnotes:
                raise ValidationError(
                    "ERR_MISSING_ESSENTIAL_FOOTNOTE",
                    "has_footnotes_or_tables is True but footnotes content is missing (violates DAT 08)"
                )

            record = PassageRecord(
                document_id=row["document_id"].strip(),
                passage_id=row["passage_id"].strip(),
                title=row["title"].strip(),
                original_reference=row.get("original_reference", "").strip(),
                language=lang,
                owner_role=row["owner_role"].strip(),
                approver_role=row["approver_role"].strip(),
                version=row["version"].strip(),
                recorded_at=recorded_at,
                effective_from=effective_from,
                effective_to=effective_to,
                status=status,
                scope_branch=row.get("scope_branch", "ALL").strip().upper(),
                scope_customer_tier=row.get("scope_customer_tier", "ALL").strip().upper(),
                scope_product_line=row.get("scope_product_line", "ALL").strip().upper(),
                superseded_by=row.get("superseded_by", "").strip() or None,
                content_text=content,
                has_footnotes_or_tables=has_footnotes,
                footnotes=footnotes
            )
            return record, None
        except ValidationError as e:
            return None, e
        except Exception as e:
            return None, ValidationError("ERR_UNEXPECTED", str(e))

class CriticalFieldValidator:
    """Validator for critical_fields.csv (Typed fields linked to exact clauses - DAT 06)"""
    REQUIRED_COLUMNS = [
        "rule_id", "clause_ref", "field_name", "field_type",
        "operator", "threshold_value", "unit_or_currency",
        "approval_role", "exception_route", "effective_from", "effective_to"
    ]

    @classmethod
    def validate_row(cls, row: Dict[str, str], row_num: int) -> Tuple[Optional[CriticalFieldRecord], Optional[ValidationError]]:
        try:
            for mandatory in ["rule_id", "clause_ref", "field_name", "operator", "threshold_value", "approval_role"]:
                if not row.get(mandatory) or not str(row[mandatory]).strip():
                    raise ValidationError("ERR_MISSING_MANDATORY_FIELD", f"Field '{mandatory}' cannot be empty")

            # Validate Operator (DAT 06)
            op_raw = row["operator"].strip()
            try:
                operator = OperatorType(op_raw)
            except ValueError:
                valid_ops = [op.value for op in OperatorType]
                raise ValidationError("ERR_INVALID_OPERATOR", f"Operator '{op_raw}' invalid. Must be one of {valid_ops}")

            # Validate FieldType
            type_raw = row.get("field_type", "number").strip().lower()
            try:
                field_type = FieldType(type_raw)
            except ValueError:
                valid_types = [t.value for t in FieldType]
                raise ValidationError("ERR_INVALID_FIELD_TYPE", f"Field type '{type_raw}' invalid. Must be one of {valid_types}")

            # Validate threshold value against type
            threshold = row["threshold_value"].strip()
            if field_type in [FieldType.NUMBER, FieldType.CURRENCY, FieldType.PERCENTAGE, FieldType.DURATION_DAYS]:
                try:
                    float(threshold)
                except ValueError:
                    raise ValidationError(
                        "ERR_INVALID_NUMERIC_VALUE",
                        f"threshold_value '{threshold}' is not a valid number for field_type '{field_type.value}'"
                    )

            effective_from = parse_iso8601(row.get("effective_from", ""), "effective_from")
            effective_to = parse_iso8601(row.get("effective_to", ""), "effective_to") or None

            record = CriticalFieldRecord(
                rule_id=row["rule_id"].strip(),
                clause_ref=row["clause_ref"].strip(),
                field_name=row["field_name"].strip(),
                field_type=field_type,
                operator=operator,
                threshold_value=threshold,
                unit_or_currency=row.get("unit_or_currency", "").strip(),
                approval_role=row["approval_role"].strip(),
                exception_route=row.get("exception_route", "").strip(),
                effective_from=effective_from,
                effective_to=effective_to
            )
            return record, None
        except ValidationError as e:
            return None, e
        except Exception as e:
            return None, ValidationError("ERR_UNEXPECTED", str(e))

class CRMContextValidator:
    """Option O1 minimal CRM context validator (DAT 07, SEC 02)"""
    REQUIRED_COLUMNS = [
        "account_id", "record_key", "customer_tier", "industry",
        "assigned_sales_role", "credit_limit_vnd", "open_warranty_tickets",
        "account_status", "updated_at"
    ]
    ALLOWED_COLUMNS = set(REQUIRED_COLUMNS)
    MAX_INITIAL_ROWS = 2000
    MAX_RETAINED_ROWS = 5000

    @classmethod
    def validate_row(cls, row: Dict[str, str], row_num: int) -> Tuple[Optional[CRMRecord], Optional[ValidationError]]:
        try:
            # Enforce allowlist: strictly forbid private correspondence, email, phone, personal dossiers
            extra_cols = set(row.keys()) - cls.ALLOWED_COLUMNS
            if extra_cols:
                raise ValidationError(
                    "ERR_UNAUTHORIZED_CRM_FIELD",
                    f"Contains unapproved CRM fields (violates SEC 02 / DAT 07): {list(extra_cols)}"
                )

            for mandatory in ["account_id", "record_key", "customer_tier", "assigned_sales_role", "updated_at"]:
                if not row.get(mandatory) or not str(row[mandatory]).strip():
                    raise ValidationError("ERR_MISSING_MANDATORY_FIELD", f"Field '{mandatory}' cannot be empty")

            credit_raw = row.get("credit_limit_vnd", "0").strip()
            try:
                credit_limit = float(credit_raw)
            except ValueError:
                raise ValidationError("ERR_INVALID_CREDIT_LIMIT", f"credit_limit_vnd '{credit_raw}' is not valid numeric")

            tickets_raw = row.get("open_warranty_tickets", "0").strip()
            try:
                tickets = int(tickets_raw)
            except ValueError:
                raise ValidationError("ERR_INVALID_TICKETS_COUNT", f"open_warranty_tickets '{tickets_raw}' is not an integer")

            updated_at = parse_iso8601(row.get("updated_at", ""), "updated_at")

            record = CRMRecord(
                account_id=row["account_id"].strip(),
                record_key=row["record_key"].strip(),
                customer_tier=row["customer_tier"].strip().upper(),
                industry=row.get("industry", "").strip(),
                assigned_sales_role=row["assigned_sales_role"].strip(),
                credit_limit_vnd=credit_limit,
                open_warranty_tickets=tickets,
                account_status=row.get("account_status", "ACTIVE").strip().upper(),
                updated_at=updated_at
            )
            return record, None
        except ValidationError as e:
            return None, e
        except Exception as e:
            return None, ValidationError("ERR_UNEXPECTED", str(e))

