"""
Data Import & Integration Engine (WP02)
Implements: WP02, DAT 01, DAT 02, DAT 06, DAT 07, DAT 08, OPS 01, VN 03

CKPA-21: Row-by-row quarantine isolation
CKPA-22: Row reconciliation (input == accepted + quarantined)
CKPA-23: Idempotent execution via SHA-256 file hash
CKPA-27: Snapshot age tracking and staleness monitoring
"""

import os
import csv
import json
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

from src.importer.models import (
    PassageRecord, CriticalFieldRecord, CRMRecord, QuarantineRecord,
    ManifestRecord, BatchType, ReconciliationStatus
)
from src.importer.validators import (
    PassageValidator, CriticalFieldValidator, CRMContextValidator
)
from src.importer.storage import StorageEngine, VN_TZ, get_now_vn_iso


class DataImportEngine:
    def __init__(self, db_path: Optional[str] = None, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.getenv("OUTPUT_DIR", "data/output")
        os.makedirs(self.output_dir, exist_ok=True)
        self.storage = StorageEngine(db_path=db_path)

    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _quarantine_rows(self, batch_id: str, file_name: str, rows: List[Dict]) -> Tuple[List, List[QuarantineRecord]]:
        """CKPA-21: Validate each row; invalid rows go to quarantine, never to active dataset."""
        accepted = []
        quarantined: List[QuarantineRecord] = []

        validator_map = {
            "passages": PassageValidator.validate_row,
            "critical_fields": CriticalFieldValidator.validate_row,
            "crm_context": CRMContextValidator.validate_row,
        }
        schema = "passages"
        if "critical" in file_name:
            schema = "critical_fields"
        elif "crm" in file_name:
            schema = "crm_context"
        validate_fn = validator_map[schema]

        for row_idx, row in enumerate(rows, start=2):
            record, err = validate_fn(row, row_idx)
            if err:
                quarantined.append(QuarantineRecord(
                    batch_id=batch_id,
                    file_name=file_name,
                    row_number=row_idx,
                    raw_data=json.dumps(row, ensure_ascii=False),
                    error_code=err.code,
                    error_reason=err.message,
                    quarantined_at=get_now_vn_iso()
                ))
            elif record:
                accepted.append(record)

        return accepted, quarantined

    def _reconcile(self, expected_rows: int, accepted_count: int, quarantined_count: int) -> ReconciliationStatus:
        """CKPA-22: Audit reconciliation: total expected == accepted + quarantined."""
        if expected_rows == (accepted_count + quarantined_count):
            return ReconciliationStatus.MATCH
        return ReconciliationStatus.MISMATCH

    def _check_idempotent(self, file_hash: str, file_name: str, batch_type: BatchType,
                          schema: str, force: bool) -> Optional[ManifestRecord]:
        """CKPA-23: Safe retry check — skip if identical SHA-256 hash was already processed."""
        if not force and self.storage.is_batch_hash_processed(file_hash):
            snapshot_info = self.storage.get_snapshot_age()
            return ManifestRecord(
                batch_id=f"cached-{file_hash[:8]}",
                batch_type=batch_type,
                schema_name=schema,
                file_name=file_name,
                file_hash_sha256=file_hash,
                timestamp=get_now_vn_iso(),
                expected_rows=0,
                accepted_rows=0,
                quarantined_rows=0,
                tombstone_rows=0,
                reconciliation_status=ReconciliationStatus.MATCH,
                snapshot_age_iso=snapshot_info["latest_snapshot_iso"] or get_now_vn_iso(),
                notes="IDEMPOTENT_SKIPPED: File already processed with identical hash."
            )
        return None

    def _export_quarantine_csv(self, batch_id: str, quarantined: List[QuarantineRecord]):
        if not quarantined:
            return
        out_file = os.path.join(self.output_dir, "quarantine_rows.csv")
        file_exists = os.path.exists(out_file)
        with open(out_file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["batch_id", "file_name", "row_number", "error_code", "error_reason", "quarantined_at", "raw_data"])
            for q in quarantined:
                writer.writerow([q.batch_id, q.file_name, q.row_number, q.error_code, q.error_reason, q.quarantined_at, q.raw_data])

    def _export_manifest(self, manifest: ManifestRecord):
        batch_manifest_file = os.path.join(self.output_dir, f"manifest_{manifest.batch_id}.json")
        with open(batch_manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, ensure_ascii=False, indent=2)

        latest_manifest_file = os.path.join(self.output_dir, "manifest_latest.json")
        with open(latest_manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, ensure_ascii=False, indent=2)

    def _read_rows(self, file_path: str) -> Tuple[str, List[Dict]]:
        rows = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        file_name = os.path.basename(file_path)
        return file_name, rows

    def _save_accepted(self, accepted, schema: str, batch_id: str) -> Tuple[int, List[str]]:
        if schema == "passages":
            return self.storage.save_passages(accepted, batch_id)
        elif schema == "critical_fields":
            return self.storage.save_critical_fields(accepted, batch_id)
        else:
            return self.storage.save_crm_records(accepted, batch_id)

    def _detect_schema(self, file_name: str) -> str:
        if "critical" in file_name:
            return "critical_fields"
        elif "crm" in file_name:
            return "crm_context"
        return "passages"

    def _build_manifest(self, batch_id: str, batch_type: BatchType, schema: str,
                        file_name: str, file_hash: str, expected_rows: int,
                        accepted_count: int, quarantined_count: int,
                        recon_status: ReconciliationStatus, notes: List[str]) -> ManifestRecord:
        snapshot_info = self.get_snapshot_age()
        return ManifestRecord(
            batch_id=batch_id,
            batch_type=batch_type,
            schema_name=schema,
            file_name=file_name,
            file_hash_sha256=file_hash,
            timestamp=get_now_vn_iso(),
            expected_rows=expected_rows,
            accepted_rows=accepted_count,
            quarantined_rows=quarantined_count,
            tombstone_rows=0,
            reconciliation_status=recon_status,
            snapshot_age_iso=snapshot_info.get("latest_snapshot_iso") or get_now_vn_iso(),
            notes="; ".join(notes) if notes else "OK"
        )

    def _import_file(self, file_path: str, batch_type: BatchType, force: bool,
                     prefix: str) -> ManifestRecord:
        file_name = os.path.basename(file_path)
        file_hash = self.calculate_sha256(file_path)
        schema = self._detect_schema(file_name)

        cached = self._check_idempotent(file_hash, file_name, batch_type, schema, force)
        if cached:
            return cached

        batch_id = f"batch-{prefix}-{uuid.uuid4().hex[:8]}"
        file_name, rows = self._read_rows(file_path)

        accepted, quarantined = self._quarantine_rows(batch_id, file_name, rows)
        expected_rows = len(rows)
        quarantined_count = len(quarantined)

        accepted_count, notes = self._save_accepted(accepted, schema, batch_id)
        self.storage.record_quarantine(quarantined)
        self._export_quarantine_csv(batch_id, quarantined)

        recon_status = self._reconcile(expected_rows, accepted_count, quarantined_count)

        manifest = self._build_manifest(
            batch_id, batch_type, schema, file_name, file_hash,
            expected_rows, accepted_count, quarantined_count, recon_status, notes
        )
        self.storage.record_batch(manifest)
        self._export_manifest(manifest)
        return manifest

    def import_passages(self, file_path: str, batch_type: BatchType = BatchType.SNAPSHOT,
                        force: bool = False) -> ManifestRecord:
        return self._import_file(file_path, batch_type, force, "pas")

    def import_critical_fields(self, file_path: str, batch_type: BatchType = BatchType.SNAPSHOT,
                                force: bool = False) -> ManifestRecord:
        return self._import_file(file_path, batch_type, force, "crit")

    def import_crm_context(self, file_path: str, batch_type: BatchType = BatchType.SNAPSHOT,
                           force: bool = False) -> ManifestRecord:
        return self._import_file(file_path, batch_type, force, "crm")

    def get_snapshot_age(self) -> Dict[str, Any]:
        """CKPA-27: Retrieve the latest successful snapshot timestamp and calculate age in human-readable and seconds format."""
        return self.storage.get_snapshot_age()
