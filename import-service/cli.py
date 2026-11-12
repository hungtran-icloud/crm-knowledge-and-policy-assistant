"""
CLI Tool for S2 (Data / Integration Engineer) in import-service
Supports:
- Importing passages, critical fields, and Option O1 CRM records
- Checking snapshot age
- Triggering immediate policy withdrawal (OPS 05, SEC 05)
"""

import sys
import os
from pathlib import Path

# Add import-service and project root to sys.path
SERVICE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SERVICE_ROOT.parent
for p in [str(SERVICE_ROOT), str(PROJECT_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import argparse
import json
from src.importer.engine import DataImportEngine
from src.importer.withdrawal import ImmediateWithdrawalService
from src.importer.models import BatchType

DEFAULT_DB = str(PROJECT_ROOT / "data" / "songnhat_knowledge.db")
DEFAULT_OUTPUT = str(PROJECT_ROOT / "data" / "output")


def main():
    parser = argparse.ArgumentParser(description="SongNhat Knowledge Ingestion CLI (WP02 / import-service)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Import Passages
    p_passages = subparsers.add_parser("import-passages", help="Import passages.csv")
    p_passages.add_argument("file", help="Path to passages CSV")
    p_passages.add_argument("--type", choices=["snapshot", "increment"], default="snapshot", help="Batch type")
    p_passages.add_argument("--force", action="store_true", help="Force import ignoring idempotency cache")

    # 2. Import Critical Fields
    p_crit = subparsers.add_parser("import-critical-fields", help="Import critical_fields.csv")
    p_crit.add_argument("file", help="Path to critical_fields CSV")
    p_crit.add_argument("--type", choices=["snapshot", "increment"], default="snapshot", help="Batch type")
    p_crit.add_argument("--force", action="store_true", help="Force import ignoring idempotency cache")

    # 3. Import CRM Context (Option O1)
    p_crm = subparsers.add_parser("import-crm", help="Import crm_context.csv (Option O1)")
    p_crm.add_argument("file", help="Path to CRM context CSV")
    p_crm.add_argument("--type", choices=["snapshot", "increment"], default="snapshot", help="Batch type")
    p_crm.add_argument("--force", action="store_true", help="Force import")

    # 4. Snapshot Age
    subparsers.add_parser("snapshot-age", help="Get snapshot age and freshness")

    # 5. Immediate Withdrawal
    p_wd = subparsers.add_parser("withdraw", help="Execute immediate policy withdrawal (OPS 05)")
    p_wd.add_argument("--type", choices=["passage", "critical_field", "crm_record"], required=True, help="Entity type")
    p_wd.add_argument("--id", required=True, help="Passage ID, Rule ID, or CRM Record Key to withdraw")
    p_wd.add_argument("--role", required=True, help="Role authorizing withdrawal (e.g., PolicyOwner_P2)")
    p_wd.add_argument("--reason", required=True, help="Detailed business reason for withdrawal")

    args = parser.parse_args()
    engine = DataImportEngine(db_path=DEFAULT_DB, output_dir=DEFAULT_OUTPUT)

    if args.command == "import-passages":
        b_type = BatchType.SNAPSHOT if args.type == "snapshot" else BatchType.INCREMENT
        manifest = engine.import_passages(args.file, batch_type=b_type, force=args.force)
        print(json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2))

    elif args.command == "import-critical-fields":
        b_type = BatchType.SNAPSHOT if args.type == "snapshot" else BatchType.INCREMENT
        manifest = engine.import_critical_fields(args.file, batch_type=b_type, force=args.force)
        print(json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2))

    elif args.command == "import-crm":
        b_type = BatchType.SNAPSHOT if args.type == "snapshot" else BatchType.INCREMENT
        manifest = engine.import_crm_context(args.file, batch_type=b_type, force=args.force)
        print(json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2))

    elif args.command == "snapshot-age":
        info = engine.storage.get_snapshot_age()
        print(json.dumps(info, ensure_ascii=False, indent=2))

    elif args.command == "withdraw":
        wd_service = ImmediateWithdrawalService(storage=engine.storage)
        if args.type == "passage":
            receipt = wd_service.withdraw_policy_passage(args.id, args.role, args.reason)
        elif args.type == "critical_field":
            receipt = wd_service.withdraw_critical_rule(args.id, args.role, args.reason)
        else:
            receipt = wd_service.withdraw_crm_record(args.id, args.role, args.reason)
        print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
