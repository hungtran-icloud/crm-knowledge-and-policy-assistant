"""
Extended test suite for WP02 in import-service:
- Critical fields quarantine isolation and reconcile
- CRM context O1 PII prevention and quarantine (DAT 07, SEC 02)
- Critical field rule and CRM record immediate withdrawal (OPS 05, SEC 05)
- Batch retrieval by ID (get_batch)
- Portable open archive export (OPS 08, DEL 04)
- Backup and restore verification (OPS 07)
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
from src.importer.models import BatchType, ReconciliationStatus

DATA_DIR = PROJECT_ROOT / "data"
TEST_DB = str(DATA_DIR / "test_extended.db")
TEST_OUTPUT = str(DATA_DIR / "test_output_ext")


class TestWP02ExtendedSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_OUTPUT, exist_ok=True)
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        cls.engine = DataImportEngine(db_path=TEST_DB, output_dir=TEST_OUTPUT)
        cls.withdrawal = ImmediateWithdrawalService(storage=cls.engine.storage)

    def test_01_critical_fields_quarantine_and_reconcile(self):
        """Test invalid critical fields are quarantined and reconciled (DAT 06)"""
        bad_crit_file = os.path.join(TEST_OUTPUT, "bad_critical_fields.csv")
        with open(bad_crit_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "rule_id", "clause_ref", "field_name", "field_type",
                "operator", "threshold_value", "unit_or_currency",
                "approval_role", "exception_route", "effective_from", "effective_to"
            ])
            # Valid row
            writer.writerow([
                "RULE-TEST-01", "Dieu 1", "discount_max", "percentage",
                "<=", "15.0", "%", "TPKD", "TGD", "2026-01-01T08:00:00+07:00", ""
            ])
            # Invalid operator
            writer.writerow([
                "RULE-TEST-02", "Dieu 2", "discount_max", "percentage",
                "INVALID_OP", "15.0", "%", "TPKD", "TGD", "2026-01-01T08:00:00+07:00", ""
            ])
            # Invalid numeric value for percentage
            writer.writerow([
                "RULE-TEST-03", "Dieu 3", "discount_max", "percentage",
                "<=", "NOT_A_NUMBER", "%", "TPKD", "TGD", "2026-01-01T08:00:00+07:00", ""
            ])

        manifest = self.engine.import_critical_fields(bad_crit_file, batch_type=BatchType.INCREMENT, force=True)
        self.assertEqual(manifest.expected_rows, 3)
        self.assertEqual(manifest.accepted_rows, 1)
        self.assertEqual(manifest.quarantined_rows, 2)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)

        # Verify get_batch
        batch_manifest = self.engine.storage.get_batch(manifest.batch_id)
        self.assertIsNotNone(batch_manifest)
        self.assertEqual(batch_manifest["batch_id"], manifest.batch_id)

    def test_02_crm_context_pii_blocking(self):
        """Test CRM context rejects rows with unauthorized PII fields (DAT 07, SEC 02)"""
        pii_crm_file = os.path.join(TEST_OUTPUT, "pii_crm.csv")
        with open(pii_crm_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            # Contains unauthorized customer_email column
            writer.writerow([
                "account_id", "record_key", "customer_tier", "industry",
                "assigned_sales_role", "credit_limit_vnd", "open_warranty_tickets",
                "account_status", "updated_at", "customer_email"
            ])
            writer.writerow([
                "ACC-001", "REC-001", "VIP", "Xay dung",
                "SalesLead_B1", "500000000", "0",
                "ACTIVE", "2026-01-01T08:00:00+07:00", "khachhang@example.com"
            ])

        manifest = self.engine.import_crm_context(pii_crm_file, batch_type=BatchType.SNAPSHOT, force=True)
        self.assertEqual(manifest.expected_rows, 1)
        self.assertEqual(manifest.accepted_rows, 0)
        self.assertEqual(manifest.quarantined_rows, 1)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)

    def test_03_withdraw_critical_rule_and_crm(self):
        """Test immediate withdrawal for critical field rule and CRM record"""
        crit_file = str(DATA_DIR / "sample" / "critical_fields.csv")
        crm_file = str(DATA_DIR / "sample" / "crm_context.csv")
        self.engine.import_critical_fields(crit_file, batch_type=BatchType.SNAPSHOT, force=True)
        self.engine.import_crm_context(crm_file, batch_type=BatchType.SNAPSHOT, force=True)

        # Withdraw critical rule
        res_crit = self.withdrawal.withdraw_critical_rule(
            rule_id="RUL-CK-01",
            role="PolicyOwner_P2",
            reason="Thu hoi han muc chiet khau TPKD"
        )
        self.assertEqual(res_crit["status"], "WITHDRAWN")

        # Withdraw CRM record
        res_crm = self.withdrawal.withdraw_crm_record(
            record_key="REC-001",
            role="DataAdmin_S2",
            reason="Yeu cau xoa du lieu khach hang theo GDPR / PDPD"
        )
        self.assertEqual(res_crm["status"], "WITHDRAWN")

    def test_04_portable_export_and_backup_restore(self):
        """Test neutral reader portable export (OPS 08) and backup/restore (OPS 07)"""
        export_dir = os.path.join(TEST_OUTPUT, "export_portable")
        manifest_export = self.engine.storage.export_portable_open_archive(export_dir)
        self.assertIn("passages", manifest_export["tables"])
        self.assertIn("critical_fields", manifest_export["tables"])

        # Test atomic backup & restore
        backup_file = os.path.join(TEST_OUTPUT, "backup.db")
        bck_res = self.engine.storage.backup_database(backup_file)
        self.assertEqual(bck_res["status"], "SUCCESS")

        res_restore = self.engine.storage.restore_database(backup_file)
        self.assertEqual(res_restore["status"], "RESTORED")


if __name__ == "__main__":
    unittest.main()

