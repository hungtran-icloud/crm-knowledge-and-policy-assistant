"""
OPS 01 Benchmark Test for WP02 in import-service:
- Tests processing 500 changed rows
- Verifies execution time << 30 minutes (Cam kết RFP)
- Verifies 100% reconciliation (MATCH)
"""

import os
import sys
import csv
import time
import unittest
from pathlib import Path

# Ensure import-service and root are in sys.path
SERVICE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SERVICE_ROOT.parent
for p in [str(SERVICE_ROOT), str(PROJECT_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from src.importer.engine import DataImportEngine
from src.importer.models import BatchType, ReconciliationStatus

DATA_DIR = PROJECT_ROOT / "data"
BENCHMARK_DB = str(DATA_DIR / "benchmark_ops01.db")
BENCHMARK_OUTPUT = str(DATA_DIR / "benchmark_output")


class TestOPS01Benchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(BENCHMARK_OUTPUT, exist_ok=True)
        if os.path.exists(BENCHMARK_DB):
            os.remove(BENCHMARK_DB)
        cls.engine = DataImportEngine(db_path=BENCHMARK_DB, output_dir=BENCHMARK_OUTPUT)

    def test_ops01_500_rows_benchmark(self):
        """OPS 01: Ingestion and reconciliation of 500 changed rows must take <= 30 minutes"""
        benchmark_csv = os.path.join(BENCHMARK_OUTPUT, "500_changed_rows.csv")
        print("\n[OPS 01] Generating 500 changed rows for benchmark...")
        
        with open(benchmark_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                'document_id', 'passage_id', 'title', 'original_reference', 'language',
                'owner_role', 'approver_role', 'version', 'recorded_at', 'effective_from',
                'effective_to', 'status', 'scope_branch', 'scope_customer_tier',
                'scope_product_line', 'superseded_by', 'content_text',
                'has_footnotes_or_tables', 'footnotes'
            ])
            for i in range(1, 501):
                writer.writerow([
                    f"DOC-BENCH-{(i // 50) + 1:02d}",
                    f"PAS-BENCH-{i:04d}",
                    f"Chính sách số {i} về điều khoản kinh doanh và kỹ thuật SongNhat",
                    f"Điều {i % 20 + 1}",
                    "vi-VN",
                    "TruongPhongKinhDoanh",
                    "GiamDocDieuHanh",
                    "1.0.0",
                    "2026-03-01T08:00:00+07:00",
                    "2026-03-01T08:00:00+07:00",
                    "",
                    "effective",
                    "ALL",
                    "VIP" if i % 3 == 0 else "ALL",
                    "DONG_CO_DIEN" if i % 2 == 0 else "BIEN_TAN",
                    "",
                    f"Nội dung quy định chi tiết cho khoản mục {i}. Áp dụng định mức kỹ thuật tiêu chuẩn cho khách hàng theo phân cấp SongNhat. Thời gian bảo hành 12 tháng kể từ ngày ký biên bản nghiệm thu.",
                    "false",
                    ""
                ])

        print(f"[OPS 01] Created {benchmark_csv} (500 rows).")

        start_time = time.perf_counter()
        manifest = self.engine.import_passages(benchmark_csv, batch_type=BatchType.SNAPSHOT, force=True)
        end_time = time.perf_counter()

        elapsed_sec = end_time - start_time
        rfp_sla_sec = 30 * 60.0  # RFP OPS 01: <= 30 minutes = 1,800 seconds

        print("\n============================================================")
        print("          BÁO CÁO KẾT QUẢ KIỂM THỬ OPS 01          ")
        print("============================================================")
        print(f"Tổng số dòng xử lý     : {manifest.accepted_rows} / {manifest.expected_rows} dòng")
        print(f"Đối soát dòng (Reconcile): {manifest.reconciliation_status.value} (100% khớp)")
        print(f"Thời gian thực thi     : {elapsed_sec:.3f} giây")
        print(f"Mục tiêu cam kết RFP   : <= {rfp_sla_sec} giây (30 phút)")
        print(f"Tốc độ xử lý           : {manifest.accepted_rows / elapsed_sec:.1f} dòng/giây")
        print(f"Đánh giá kết quả       : {'ĐẠT CHUẨN VƯỢT MỨC (PASSED)' if elapsed_sec <= rfp_sla_sec else 'FAILED'}")
        print("============================================================\n")

        self.assertEqual(manifest.expected_rows, 500)
        self.assertEqual(manifest.accepted_rows, 500)
        self.assertEqual(manifest.quarantined_rows, 0)
        self.assertEqual(manifest.reconciliation_status, ReconciliationStatus.MATCH)
        self.assertLess(elapsed_sec, rfp_sla_sec)


if __name__ == "__main__":
    unittest.main()

