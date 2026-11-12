"""
Batch import API — WP02.
Implements: WP02, DAT01-02, DAT06, DAT07, DAT08, OPS01
Wires DataImportEngine from src.importer.
"""
import os
import shutil
import tempfile
from enum import Enum
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from pydantic import BaseModel

from src.importer.engine import DataImportEngine
from src.importer.models import BatchType as ImporterBatchType, ReconciliationStatus

router = APIRouter()


class BatchType(str, Enum):
    snapshot = "snapshot"
    increment = "increment"


class BatchSubmitResponse(BaseModel):
    batch_id: str
    status: str
    message: str


class BatchStatusResponse(BaseModel):
    batch_id: str
    schema_name: str
    expected_rows: int
    accepted_rows: int
    quarantined_rows: int
    reconciliation_status: str
    snapshot_age_iso: str
    notes: str


def _save_upload_to_temp(file: UploadFile) -> str:
    """Helper to save uploaded file stream into a temporary file on disk."""
    suffix = os.path.splitext(file.filename or "data.csv")[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        shutil.copyfileobj(file.file, tmp)
        tmp.flush()
        return tmp.name
    finally:
        tmp.close()


@router.post(
    "/passages",
    response_model=BatchSubmitResponse,
    status_code=202,
    summary="Submit passages.csv batch (WP02, DAT01-02, DAT08, OPS01)",
)
async def submit_passages_batch(
    file: UploadFile = File(..., description="UTF-8 CSV, max 500 changed rows (OPS01)"),
    batch_type: BatchType = Query(BatchType.snapshot),
    force: bool = Query(False, description="Force reprocess even if file hash seen"),
):
    """
    Submit a passages CSV batch for import.
    - Validates schema, quarantines invalid rows, reconciles expected vs accepted.
    - Idempotent via SHA-256 file hash (DAT02).
    """
    temp_path = _save_upload_to_temp(file)
    try:
        engine = DataImportEngine()
        b_type = ImporterBatchType.SNAPSHOT if batch_type == BatchType.snapshot else ImporterBatchType.INCREMENT
        manifest = engine.import_passages(temp_path, batch_type=b_type, force=force)
        status = "accepted" if manifest.reconciliation_status == ReconciliationStatus.MATCH else "mismatch"
        return BatchSubmitResponse(
            batch_id=manifest.batch_id,
            status=status,
            message=manifest.notes or "Passages batch processed successfully"
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post(
    "/critical-fields",
    response_model=BatchSubmitResponse,
    status_code=202,
    summary="Submit critical_fields.csv batch (WP02, DAT06)",
)
async def submit_critical_fields_batch(
    file: UploadFile = File(...),
    batch_type: BatchType = Query(BatchType.snapshot),
    force: bool = Query(False),
):
    temp_path = _save_upload_to_temp(file)
    try:
        engine = DataImportEngine()
        b_type = ImporterBatchType.SNAPSHOT if batch_type == BatchType.snapshot else ImporterBatchType.INCREMENT
        manifest = engine.import_critical_fields(temp_path, batch_type=b_type, force=force)
        status = "accepted" if manifest.reconciliation_status == ReconciliationStatus.MATCH else "mismatch"
        return BatchSubmitResponse(
            batch_id=manifest.batch_id,
            status=status,
            message=manifest.notes or "Critical fields batch processed successfully"
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post(
    "/crm-context",
    response_model=BatchSubmitResponse,
    status_code=202,
    summary="Submit CRM context batch (Option O1, DAT07, SEC02)",
)
async def submit_crm_context_batch(
    file: UploadFile = File(...),
    batch_type: BatchType = Query(BatchType.snapshot),
    force: bool = Query(False),
):
    """
    Option O1 only — separately priced.
    Enable only after identity, permissions, lawful processing verified (DAT07, SEC02).
    """
    temp_path = _save_upload_to_temp(file)
    try:
        engine = DataImportEngine()
        b_type = ImporterBatchType.SNAPSHOT if batch_type == BatchType.snapshot else ImporterBatchType.INCREMENT
        manifest = engine.import_crm_context(temp_path, batch_type=b_type, force=force)
        status = "accepted" if manifest.reconciliation_status == ReconciliationStatus.MATCH else "mismatch"
        return BatchSubmitResponse(
            batch_id=manifest.batch_id,
            status=status,
            message=manifest.notes or "CRM context batch processed successfully"
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/snapshot-age", summary="Get data freshness (DAT02)")
async def get_snapshot_age():
    """Returns age of the latest snapshot."""
    engine = DataImportEngine()
    return engine.storage.get_snapshot_age()


@router.get("/{batch_id}", response_model=BatchStatusResponse, summary="Get batch manifest")
async def get_batch_status(batch_id: str):
    """Retrieves batch processing manifest and reconciliation state."""
    engine = DataImportEngine()
    batch = engine.storage.get_batch(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch '{batch_id}' not found")
    return BatchStatusResponse(
        batch_id=batch["batch_id"],
        schema_name=batch["schema_name"],
        expected_rows=batch["expected_rows"],
        accepted_rows=batch["accepted_rows"],
        quarantined_rows=batch["quarantined_rows"],
        reconciliation_status=batch["reconciliation_status"],
        snapshot_age_iso=batch.get("snapshot_age_iso") or "",
        notes=batch.get("notes") or ""
    )
