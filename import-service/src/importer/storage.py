"""
Storage and repository layer using SQLite
Implements: DAT 01 (provenance), DAT 02 (tombstone & version history), OPS 05 (withdrawal), OPS 07 (restore), WP02

CKPA-24: Tombstone mechanism — explicit deletion markers.
CKPA-25: Version history — preserves document and passage version history without silent overwrite.
"""

import sqlite3
import json
import os
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Tuple
from src.importer.models import (
    PassageRecord, CriticalFieldRecord, CRMRecord,
    QuarantineRecord, ManifestRecord, TombstoneRecord, PolicyStatus
)

VN_TZ = timezone(timedelta(hours=7))

def get_now_vn_iso() -> str:
    return datetime.now(VN_TZ).isoformat()

class StorageEngine:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DATABASE_PATH", "data/songnhat_knowledge.db")
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            c = conn.cursor()
            # 1. Passages table
            c.execute("""
                CREATE TABLE IF NOT EXISTS passages (
                    passage_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    original_reference TEXT,
                    language TEXT DEFAULT 'vi-VN',
                    owner_role TEXT NOT NULL,
                    approver_role TEXT NOT NULL,
                    version TEXT NOT NULL,
                    recorded_at TEXT,
                    effective_from TEXT,
                    effective_to TEXT,
                    status TEXT NOT NULL,
                    scope_branch TEXT DEFAULT 'ALL',
                    scope_customer_tier TEXT DEFAULT 'ALL',
                    scope_product_line TEXT DEFAULT 'ALL',
                    superseded_by TEXT,
                    content_text TEXT NOT NULL,
                    has_footnotes_or_tables INTEGER DEFAULT 0,
                    footnotes TEXT,
                    is_tombstone INTEGER DEFAULT 0,
                    updated_at TEXT NOT NULL
                )
            """)

            # 2. Critical Fields table
            c.execute("""
                CREATE TABLE IF NOT EXISTS critical_fields (
                    rule_id TEXT PRIMARY KEY,
                    clause_ref TEXT NOT NULL,
                    field_name TEXT NOT NULL,
                    field_type TEXT NOT NULL,
                    operator TEXT NOT NULL,
                    threshold_value TEXT NOT NULL,
                    unit_or_currency TEXT,
                    approval_role TEXT NOT NULL,
                    exception_route TEXT,
                    effective_from TEXT,
                    effective_to TEXT,
                    is_tombstone INTEGER DEFAULT 0,
                    updated_at TEXT NOT NULL
                )
            """)

            # 3. CRM minimal context table (Option O1)
            c.execute("""
                CREATE TABLE IF NOT EXISTS crm_records (
                    record_key TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL,
                    customer_tier TEXT NOT NULL,
                    industry TEXT,
                    assigned_sales_role TEXT,
                    credit_limit_vnd REAL,
                    open_warranty_tickets INTEGER,
                    account_status TEXT,
                    updated_at TEXT NOT NULL
                )
            """)

            # 4. Version History (CKPA-25, DAT 01, DAT 02)
            c.execute("""
                CREATE TABLE IF NOT EXISTS version_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    batch_id TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )
            """)

            # 5. Tombstones (CKPA-24, DAT 02)
            c.execute("""
                CREATE TABLE IF NOT EXISTS tombstones (
                    tombstone_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    tombstone_at TEXT NOT NULL,
                    tombstone_by_role TEXT NOT NULL,
                    reason TEXT NOT NULL
                )
            """)

            # 6. Batches and Idempotency (DAT 02)
            c.execute("""
                CREATE TABLE IF NOT EXISTS batches (
                    batch_id TEXT PRIMARY KEY,
                    file_hash_sha256 TEXT NOT NULL,
                    batch_type TEXT NOT NULL,
                    schema_name TEXT NOT NULL,
                    manifest_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # 7. Quarantine records (DAT 08)
            c.execute("""
                CREATE TABLE IF NOT EXISTS quarantine_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    row_number INTEGER NOT NULL,
                    raw_data TEXT NOT NULL,
                    error_code TEXT NOT NULL,
                    error_reason TEXT NOT NULL,
                    quarantined_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def is_batch_hash_processed(self, file_hash: str) -> bool:
        """Idempotent check: has this exact file already been imported?"""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT batch_id FROM batches WHERE file_hash_sha256 = ?", (file_hash,))
            return c.fetchone() is not None

    def record_batch(self, manifest: ManifestRecord):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO batches (batch_id, file_hash_sha256, batch_type, schema_name, manifest_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                manifest.batch_id,
                manifest.file_hash_sha256,
                manifest.batch_type.value,
                manifest.schema_name,
                json.dumps(manifest.to_dict(), ensure_ascii=False),
                manifest.timestamp
            ))
            conn.commit()

    def record_quarantine(self, records: List[QuarantineRecord]):
        if not records:
            return
        with self._get_conn() as conn:
            c = conn.cursor()
            c.executemany("""
                INSERT INTO quarantine_records (batch_id, file_name, row_number, raw_data, error_code, error_reason, quarantined_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                (r.batch_id, r.file_name, r.row_number, r.raw_data, r.error_code, r.error_reason, r.quarantined_at)
                for r in records
            ])
            conn.commit()

    def save_passages(self, records: List[PassageRecord], batch_id: str) -> Tuple[int, List[str]]:
        """
        Saves passages with version checking (CKPA-25):
        - If existing has higher version, reject overwrite (DAT 02).
        - Saves previous version to version_history.
        """
        accepted = 0
        skipped_notes = []
        now_vn = get_now_vn_iso()

        with self._get_conn() as conn:
            c = conn.cursor()
            for r in records:
                # Check existing version
                c.execute("SELECT version, status, is_tombstone FROM passages WHERE passage_id = ?", (r.passage_id,))
                existing = c.fetchone()
                if existing:
                    existing_ver = existing["version"]
                    # If late batch has smaller version, ignore overwrite
                    if r.version < existing_ver:
                        skipped_notes.append(f"Passage {r.passage_id}: incoming version {r.version} older than {existing_ver}, ignored overwrite")
                        continue

                    # Record old version into version_history before updating (CKPA-25)
                    c.execute("SELECT * FROM passages WHERE passage_id = ?", (r.passage_id,))
                    old_row = dict(c.fetchone())
                    c.execute("""
                        INSERT INTO version_history (entity_type, entity_id, version, status, payload_json, batch_id, recorded_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('passage', r.passage_id, existing_ver, old_row['status'], json.dumps(old_row, ensure_ascii=False), batch_id, now_vn))

                # Upsert current record
                c.execute("""
                    INSERT OR REPLACE INTO passages (
                        passage_id, document_id, title, original_reference, language,
                        owner_role, approver_role, version, recorded_at, effective_from,
                        effective_to, status, scope_branch, scope_customer_tier,
                        scope_product_line, superseded_by, content_text,
                        has_footnotes_or_tables, footnotes, is_tombstone, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """, (
                    r.passage_id, r.document_id, r.title, r.original_reference, r.language,
                    r.owner_role, r.approver_role, r.version, r.recorded_at or now_vn, r.effective_from,
                    r.effective_to, r.status.value, r.scope_branch, r.scope_customer_tier,
                    r.scope_product_line, r.superseded_by, r.content_text,
                    1 if r.has_footnotes_or_tables else 0, r.footnotes, now_vn
                ))
                accepted += 1
            conn.commit()
        return accepted, skipped_notes

    def save_critical_fields(self, records: List[CriticalFieldRecord], batch_id: str) -> Tuple[int, List[str]]:
        accepted = 0
        skipped_notes = []
        now_vn = get_now_vn_iso()

        with self._get_conn() as conn:
            c = conn.cursor()
            for r in records:
                c.execute("SELECT * FROM critical_fields WHERE rule_id = ?", (r.rule_id,))
                existing = c.fetchone()
                if existing:
                    old_row = dict(existing)
                    c.execute("""
                        INSERT INTO version_history (entity_type, entity_id, version, status, payload_json, batch_id, recorded_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('critical_field', r.rule_id, "active", "updated", json.dumps(old_row, ensure_ascii=False), batch_id, now_vn))

                c.execute("""
                    INSERT OR REPLACE INTO critical_fields (
                        rule_id, clause_ref, field_name, field_type, operator,
                        threshold_value, unit_or_currency, approval_role,
                        exception_route, effective_from, effective_to, is_tombstone, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """, (
                    r.rule_id, r.clause_ref, r.field_name, r.field_type.value, r.operator.value,
                    r.threshold_value, r.unit_or_currency, r.approval_role,
                    r.exception_route, r.effective_from, r.effective_to, now_vn
                ))
                accepted += 1
            conn.commit()
        return accepted, skipped_notes

    def save_crm_records(self, records: List[CRMRecord], batch_id: str) -> Tuple[int, List[str]]:
        accepted = 0
        skipped_notes = []
        now_vn = get_now_vn_iso()

        with self._get_conn() as conn:
            c = conn.cursor()
            # Enforce max 5,000 retained rows constraint (DAT 07)
            c.execute("SELECT COUNT(*) FROM crm_records")
            current_count = c.fetchone()[0]
            if current_count + len(records) > 5000:
                raise ValueError(f"Exceeds maximum 5,000 retained CRM rows limit (currently {current_count})")

            for r in records:
                c.execute("""
                    INSERT OR REPLACE INTO crm_records (
                        record_key, account_id, customer_tier, industry,
                        assigned_sales_role, credit_limit_vnd, open_warranty_tickets,
                        account_status, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.record_key, r.account_id, r.customer_tier, r.industry,
                    r.assigned_sales_role, r.credit_limit_vnd, r.open_warranty_tickets,
                    r.account_status, r.updated_at or now_vn
                ))
                accepted += 1
            conn.commit()
        return accepted, skipped_notes

    def immediate_withdraw(self, entity_type: str, entity_id: str, role: str, reason: str) -> bool:
        """
        Kênh withdrawal tức thời (WP02, OPS 05, SEC 05):
        Ngay lập tức đánh dấu entity sang trạng thái WITHDRAWN và ghi nhận Tombstone.
        """
        now_vn = get_now_vn_iso()
        with self._get_conn() as conn:
            c = conn.cursor()
            if entity_type == "passage":
                c.execute("SELECT * FROM passages WHERE passage_id = ?", (entity_id,))
                row = c.fetchone()
                if not row:
                    return False
                c.execute("""
                    UPDATE passages 
                    SET status = ?, is_tombstone = 1, updated_at = ?
                    WHERE passage_id = ?
                """, (PolicyStatus.WITHDRAWN.value, now_vn, entity_id))
            elif entity_type == "critical_field":
                c.execute("SELECT * FROM critical_fields WHERE rule_id = ?", (entity_id,))
                row = c.fetchone()
                if not row:
                    return False
                c.execute("""
                    UPDATE critical_fields 
                    SET is_tombstone = 1, updated_at = ?
                    WHERE rule_id = ?
                """, (now_vn, entity_id))
            elif entity_type == "crm_record":
                c.execute("SELECT * FROM crm_records WHERE record_key = ?", (entity_id,))
                row = c.fetchone()
                if not row:
                    return False
                c.execute("DELETE FROM crm_records WHERE record_key = ?", (entity_id,))
            else:
                return False

            # Add to tombstones log
            c.execute("""
                INSERT INTO tombstones (entity_type, entity_id, tombstone_at, tombstone_by_role, reason)
                VALUES (?, ?, ?, ?, ?)
            """, (entity_type, entity_id, now_vn, role, reason))

            conn.commit()
            return True

    def get_batch(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves manifest of a specific batch by ID (WP02)"""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT manifest_json FROM batches WHERE batch_id = ?", (batch_id,))
            row = c.fetchone()
            if row:
                return json.loads(row["manifest_json"])
            return None

    def get_snapshot_age(self) -> Dict[str, Any]:
        """Returns the latest snapshot age and timestamp (WP02, Section 2)"""
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT created_at FROM batches ORDER BY created_at DESC LIMIT 1")
            row = c.fetchone()
            if not row:
                return {
                    "has_snapshot": False,
                    "latest_snapshot_iso": None,
                    "age_seconds": None,
                    "age_human": "Chưa có snapshot nào được nạp"
                }
            latest_iso = row["created_at"]
            try:
                latest_dt = datetime.fromisoformat(latest_iso)
                now_dt = datetime.now(VN_TZ)
                diff = now_dt - latest_dt
                age_sec = max(0, int(diff.total_seconds()))
                hours = age_sec // 3600
                mins = (age_sec % 3600) // 60
                age_human = f"{hours} giờ {mins} phút trước" if hours > 0 else f"{mins} phút trước"
            except Exception:
                age_sec = None
                age_human = latest_iso

            return {
                "has_snapshot": True,
                "latest_snapshot_iso": latest_iso,
                "age_seconds": age_sec,
                "age_human": age_human
            }

    def get_active_passage(self, passage_id: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM passages WHERE passage_id = ? AND is_tombstone = 0 AND status != 'withdrawn'", (passage_id,))
            row = c.fetchone()
            return dict(row) if row else None

    # =========================================================================
    # QUERY INTERFACE FOR S3 (POLICY ENGINE) - DAT 04, ANS 02, KNW 03, OPS 03
    # =========================================================================

    def query_effective_passages(
        self,
        governing_date_iso: Optional[str] = None,
        branch: str = "ALL",
        customer_tier: str = "ALL",
        product_line: str = "ALL",
        keyword: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        check_date = governing_date_iso or get_now_vn_iso()
        query = """
            SELECT * FROM passages
            WHERE is_tombstone = 0
              AND status IN ('effective', 'approved')
              AND (effective_from IS NULL OR effective_from <= ?)
              AND (effective_to IS NULL OR effective_to >= ?)
              AND (scope_branch = 'ALL' OR ? = 'ALL' OR scope_branch = ?)
              AND (scope_customer_tier = 'ALL' OR ? = 'ALL' OR scope_customer_tier = ?)
              AND (scope_product_line = 'ALL' OR ? = 'ALL' OR scope_product_line = ?)
        """
        params = [
            check_date, check_date,
            branch, branch,
            customer_tier, customer_tier,
            product_line, product_line
        ]

        if keyword:
            query += " AND (title LIKE ? OR content_text LIKE ?)"
            kw_param = f"%{keyword}%"
            params.extend([kw_param, kw_param])

        query += " ORDER BY effective_from DESC LIMIT ?"
        params.append(limit)

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute(query, params)
            return [dict(row) for row in c.fetchall()]

    def get_critical_fields_for_clause(
        self,
        clause_ref: str,
        governing_date_iso: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        check_date = governing_date_iso or get_now_vn_iso()
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT * FROM critical_fields
                WHERE clause_ref = ?
                  AND is_tombstone = 0
                  AND (effective_from IS NULL OR effective_from <= ?)
                  AND (effective_to IS NULL OR effective_to >= ?)
                ORDER BY rule_id ASC
            """, (clause_ref, check_date, check_date))
            return [dict(row) for row in c.fetchall()]

    # =========================================================================
    # PORTABLE EXPORT FOR EXIT & NEUTRAL READER (OPS 08, DEL 04)
    # =========================================================================

    def export_portable_open_archive(self, export_dir: str = "data/export_neutral") -> Dict[str, Any]:
        os.makedirs(export_dir, exist_ok=True)
        manifest_export = {"exported_at": get_now_vn_iso(), "tables": {}}

        tables = ["passages", "critical_fields", "crm_records", "version_history", "tombstones", "batches"]
        with self._get_conn() as conn:
            c = conn.cursor()
            for tbl in tables:
                c.execute(f"SELECT * FROM {tbl}")
                rows = [dict(row) for row in c.fetchall()]
                target_file = os.path.join(export_dir, f"{tbl}.json")
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(rows, f, ensure_ascii=False, indent=2)
                manifest_export["tables"][tbl] = {
                    "count": len(rows),
                    "file": target_file
                }

        manifest_path = os.path.join(export_dir, "export_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_export, f, ensure_ascii=False, indent=2)

        return manifest_export

    # =========================================================================
    # BACKUP & RESTORE FOR OPS 07 (RPO 24h, RTO 4h)
    # =========================================================================

    def backup_database(self, backup_file_path: str) -> Dict[str, Any]:
        os.makedirs(os.path.dirname(os.path.abspath(backup_file_path)), exist_ok=True)
        with self._get_conn() as src_conn:
            bck_conn = sqlite3.connect(backup_file_path)
            src_conn.backup(bck_conn)
            bck_conn.close()

        return {
            "backup_file": backup_file_path,
            "backup_time": get_now_vn_iso(),
            "status": "SUCCESS"
        }

    def restore_database(self, backup_file_path: str) -> Dict[str, Any]:
        if not os.path.exists(backup_file_path):
            raise FileNotFoundError(f"Backup file not found: {backup_file_path}")

        test_conn = sqlite3.connect(backup_file_path)
        cur = test_conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        check_result = cur.fetchone()[0]
        test_conn.close()

        if check_result != "ok":
            raise ValueError(f"Backup file integrity check failed: {check_result}")

        with sqlite3.connect(backup_file_path) as src_conn:
            target_conn = self._get_conn()
            src_conn.backup(target_conn)
            target_conn.close()

        return {
            "restored_from": backup_file_path,
            "restored_at": get_now_vn_iso(),
            "integrity_check": check_result,
            "status": "RESTORED"
        }
