"""
Comprehensive test suite for WP02 in import-service:
- Two CSV validators (passages & critical_fields) + O1 validator (crm_context)
- Manifest generation and structure
- Quarantine isolation (DAT 08)
- Reconciliation integrity (DAT 02)
- Idempotent retries
- Version history & late batch protection
- Immediate withdrawal channel & tombstones (OPS 05, SEC 05)
- Snapshot age tracking
"""

import os
import sys
import csv
import json
import unittest
from pathlib import Path

# Ensure import-service and root are in sys.path
SERVICE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SERVICE_ROOT.parent
for p in [str(SERVICE_ROOT), str(PROJECT_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from src.importer.engine import DataImportEngine
from src.importer.withdrawal import ImmediateWithdrawalService
from src.importer.models import BatchType, ReconciliationStatus, PolicyStatus

DATA_DIR = PROJECT_ROOT / "data"
TEST_DB = str(DATA_DIR / "test_songnhat.db")
TEST_OUTPUT = str(DATA_DIR / "test_output")


class TestWP02IntegrationSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_OUTPUT, exist_ok=True)
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        cls.engine = DataImportEngine(db_path=TEST_DB, output_dir=TEST_OUTPUT)
        cls.withdrawal_service = ImmediateWithdrawalService(storage=cls.engine.storage)

    def test_01_import_valid_passages(self):
        """Test importing the 30 curated passages for Gate G0"""
        passages_file = str(DATA_DIR / "sample" / "passages.csv")
        manifest = self.engine.import_passages(passages_file, batch_type=BatchType.SNAPSHOT)
        
        self.assertEqual(manifest.expected_rows, 30)
        self.assertEqual(manifest.accepted_rows, 30)
        self.assertEqual(manifest.quarantined_rows, 0)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)
        self.assertTrue(manifest.file_hash_sha256)
        print("\n[TEST 01 PASSED] 30 passages imported and reconciled 100%.")

    def test_02_import_valid_critical_fields(self):
        """Test importing the 10 critical field rules for Gate G0"""
        crit_file = str(DATA_DIR / "sample" / "critical_fields.csv")
        manifest = self.engine.import_critical_fields(crit_file, batch_type=BatchType.SNAPSHOT)
        
        self.assertEqual(manifest.expected_rows, 10)
        self.assertEqual(manifest.accepted_rows, 10)
        self.assertEqual(manifest.quarantined_rows, 0)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)
        print("[TEST 02 PASSED] 10 critical fields imported and reconciled 100%.")

    def test_03_import_valid_crm_context_o1(self):
        """Test importing Option O1 minimal CRM context"""
        crm_file = str(DATA_DIR / "sample" / "crm_context.csv")
        manifest = self.engine.import_crm_context(crm_file, batch_type=BatchType.SNAPSHOT)
        
        self.assertEqual(manifest.expected_rows, 5)
        self.assertEqual(manifest.accepted_rows, 5)
        self.assertEqual(manifest.quarantined_rows, 0)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)
        print("[TEST 03 PASSED] 5 Option O1 CRM records imported and reconciled.")

    def test_04_idempotent_retry(self):
        """Test re-importing the identical file skips without duplicating records (DAT 02)"""
        passages_file = str(DATA_DIR / "sample" / "passages.csv")
        manifest = self.engine.import_passages(passages_file, batch_type=BatchType.SNAPSHOT, force=False)
        self.assertIn("IDEMPOTENT_SKIPPED", manifest.notes)
        print("[TEST 04 PASSED] Idempotent retry detected identical file hash and skipped safely.")

    def test_05_quarantine_isolation_and_reconciliation(self):
        """Test bad rows are isolated into quarantine without failing accepted rows (DAT 02, DAT 08)"""
        bad_csv_path = str(DATA_DIR / "test_output" / "bad_passages.csv")
        rows = [
            # Row 1: Valid
            ["DOC-TEST", "PAS-OK-01", "Tieu de tot", "Dieu 1", "vi-VN", "TPKD", "TGĐ", "1.0.0", "2026-01-01T08:00:00+07:00", "2026-01-01T08:00:00+07:00", "", "effective", "ALL", "ALL", "ALL", "", "Noi dung chuan", "false", ""],
            # Row 2: Invalid - missing mandatory field (approver_role is empty)
            ["DOC-TEST", "PAS-ERR-01", "Thieu nguoi duyet", "Dieu 2", "vi-VN", "TPKD", "", "1.0.0", "2026-01-01T08:00:00+07:00", "2026-01-01T08:00:00+07:00", "", "effective", "ALL", "ALL", "ALL", "", "Noi dung", "false", ""],
            # Row 3: Invalid - exceeds 6,000 characters cap (DAT 08)
            ["DOC-TEST", "PAS-ERR-02", "Noi dung qua dai", "Dieu 3", "vi-VN", "TPKD", "TGĐ", "1.0.0", "2026-01-01T08:00:00+07:00", "2026-01-01T08:00:00+07:00", "", "effective", "ALL", "ALL", "ALL", "", "A" * 6005, "false", ""],
            # Row 4: Invalid - has_footnotes_or_tables is True but footnotes is empty (DAT 08)
            ["DOC-TEST", "PAS-ERR-03", "Thieu cuoc chu", "Dieu 4", "vi-VN", "TPKD", "TGĐ", "1.0.0", "2026-01-01T08:00:00+07:00", "2026-01-01T08:00:00+07:00", "", "effective", "ALL", "ALL", "ALL", "", "Noi dung co cuoc chu", "true", ""],
            # Row 5: Valid
            ["DOC-TEST", "PAS-OK-02", "Tieu de tot 2", "Dieu 5", "vi-VN", "TPKD", "TGĐ", "1.0.0", "2026-01-01T08:00:00+07:00", "2026-01-01T08:00:00+07:00", "", "effective", "ALL", "ALL", "ALL", "", "Noi dung chuan 2", "false", ""]
        ]

        with open(bad_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                'document_id', 'passage_id', 'title', 'original_reference', 'language',
                'owner_role', 'approver_role', 'version', 'recorded_at', 'effective_from',
                'effective_to', 'status', 'scope_branch', 'scope_customer_tier',
                'scope_product_line', 'superseded_by', 'content_text',
                'has_footnotes_or_tables', 'footnotes'
            ])
            for r in rows:
                writer.writerow(r)

        manifest = self.engine.import_passages(bad_csv_path, batch_type=BatchType.INCREMENT, force=True)

        self.assertEqual(manifest.expected_rows, 5)
        self.assertEqual(manifest.accepted_rows, 2)
        self.assertEqual(manifest.quarantined_rows, 3)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)
        print("[TEST 05 PASSED] 3 bad rows quarantined, 2 valid rows accepted. Reconcile = MATCH.")

    def test_06_version_history_and_late_batch_protection(self):
        """Test version update and ensure older version cannot overwrite newer version (DAT 02)"""
        v2_path = str(DATA_DIR / "test_output" / "v2_passage.csv")
        with open(v2_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                'document_id', 'passage_id', 'title', 'original_reference', 'language',
                'owner_role', 'approver_role', 'version', 'recorded_at', 'effective_from',
                'effective_to', 'status', 'scope_branch', 'scope_customer_tier',
                'scope_product_line', 'superseded_by', 'content_text',
                'has_footnotes_or_tables', 'footnotes'
            ])
            # Update PAS-BG-01 to version 2.0.0
            writer.writerow([
                'DOC-BG-01', 'PAS-BG-01', 'Quy trinh cap nhat 2.0', 'Dieu 1 moi', 'vi-VN',
                'TPKD', 'TGĐ', '2.0.0', '2026-02-01T08:00:00+07:00', '2026-02-01T08:00:00+07:00',
                '', 'effective', 'ALL', 'ALL', 'DONG_CO_DIEN', '', 'Noi dung phien ban 2.0', 'false', ''
            ])
        m2 = self.engine.import_passages(v2_path, batch_type=BatchType.INCREMENT, force=True)
        self.assertEqual(m2.accepted_rows, 1)

        # Check DB has v2.0.0
        active_p = self.engine.storage.get_active_passage("PAS-BG-01")
        self.assertEqual(active_p["version"], "2.0.0")

        # Now simulate a late batch arriving with older version 1.2.0
        v_late_path = str(DATA_DIR / "test_output" / "late_passage.csv")
        with open(v_late_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                'document_id', 'passage_id', 'title', 'original_reference', 'language',
                'owner_role', 'approver_role', 'version', 'recorded_at', 'effective_from',
                'effective_to', 'status', 'scope_branch', 'scope_customer_tier',
                'scope_product_line', 'superseded_by', 'content_text',
                'has_footnotes_or_tables', 'footnotes'
            ])
            writer.writerow([
                'DOC-BG-01', 'PAS-BG-01', 'Quy trinh cu di tre', 'Dieu 1 cu', 'vi-VN',
                'TPKD', 'TGĐ', '1.2.0', '2026-01-15T08:00:00+07:00', '2026-01-15T08:00:00+07:00',
                '', 'effective', 'ALL', 'ALL', 'DONG_CO_DIEN', '', 'Noi dung cu', 'false', ''
            ])
        m_late = self.engine.import_passages(v_late_path, batch_type=BatchType.INCREMENT, force=True)
        self.assertEqual(m_late.accepted_rows, 0)
        self.assertIn("older than 2.0.0, ignored overwrite", m_late.notes)

        # Check DB still retains v2.0.0
        active_p_after = self.engine.storage.get_active_passage("PAS-BG-01")
        self.assertEqual(active_p_after["version"], "2.0.0")
        print("[TEST 06 PASSED] Version history tracked and late batch overwrite prevented.")

    def test_07_immediate_withdrawal_and_tombstone(self):
        """Test immediate withdrawal bypasses daily batch and marks tombstone (OPS 05, SEC 05)"""
        # Ensure PAS-BG-02 is currently active
        p_before = self.engine.storage.get_active_passage("PAS-BG-02")
        self.assertIsNotNone(p_before)

        cache_purge_called = []
        def on_cache_purge(entity_type, entity_id):
            cache_purge_called.append((entity_type, entity_id))

        self.withdrawal_service.register_cache_purge_listener(on_cache_purge)

        # Immediate withdrawal by Policy Owner
        receipt = self.withdrawal_service.withdraw_policy_passage(
            passage_id="PAS-BG-02",
            role="PolicyOwner_P2",
            reason="Chinh sach bi thu hoi khan cap do thay doi bieu phi 2026"
        )

        self.assertEqual(receipt["status"], "WITHDRAWN")
        self.assertTrue(receipt["cache_purged"])
        self.assertEqual(len(cache_purge_called), 1)
        self.assertEqual(cache_purge_called[0], ("passage", "PAS-BG-02"))

        # Subsequent retrieval must return None (blocked)
        p_after = self.engine.storage.get_active_passage("PAS-BG-02")
        self.assertIsNone(p_after)
        print("[TEST 07 PASSED] Immediate withdrawal executed instantly, tombstone created, cache purged.")

    def test_08_snapshot_age(self):
        """Test snapshot age calculation (WP02)"""
        info = self.engine.storage.get_snapshot_age()
        self.assertTrue(info["has_snapshot"])
        self.assertIsNotNone(info["age_seconds"])
        print(f"[TEST 08 PASSED] Snapshot age queried: {info['age_human']} ({info['latest_snapshot_iso']})")


if __name__ == "__main__":
    unittest.main()

