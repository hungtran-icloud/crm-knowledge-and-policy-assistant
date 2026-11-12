# Gói Công Việc WP02: Data Import & Integration Engine
**Phụ trách:** S2 (Data / Integration Engineer) | **Hỗ trợ:** P4, S5

Hệ thống xử lý nhập liệu, đối soát tính toàn vẹn dữ liệu, cô lập dòng lỗi và quản lý vòng đời chính sách cho **SongNhat CRM Knowledge and Policy Assistant**, tuân thủ 100% các tiêu chuẩn trong Hồ sơ mời thầu (RFP).

---

## 1. Cấu Trúc Thư Mục Triển Khai Trong `import-service`
```
├── data/
│   ├── templates/               # Schema mẫu chuẩn UTF-8
│   │   ├── passages_template.csv
│   │   ├── critical_fields_template.csv
│   │   └── crm_context_template.csv (Option O1)
│   ├── sample/                  # Bộ dữ liệu mẫu chuẩn bị cho Cổng G0
│   │   ├── passages.csv         # 30 đoạn trích chính sách chuẩn
│   │   ├── critical_fields.csv  # 10 trường thông số ngưỡng & thẩm quyền
│   │   └── crm_context.csv      # Dữ liệu CRM mẫu cho Option O1
│   └── output/                  # Vùng xuất báo cáo vận hành
│       ├── manifest_latest.json # Manifest mẻ nạp gần nhất
│       └── quarantine_rows.csv  # Dòng bị cô lập kèm mã lỗi
├── import-service/              # Toàn bộ mã nguồn & kiểm thử của S2
│   ├── src/
│   │   ├── importer/            # Core logic nạp & kiểm soát chất lượng
│   │   │   ├── models.py        # Dataclasses & Enum trạng thái
│   │   │   ├── validators.py    # 3 bộ kiểm tra hợp lệ cú pháp & ngữ nghĩa
│   │   │   ├── storage.py       # Quản lý cơ sở dữ liệu SQLite & Provenance
│   │   │   ├── engine.py        # Điều phối nạp, đối soát và idempotent
│   │   │   └── withdrawal.py    # Kênh thu hồi chính sách tức thời
│   │   ├── api/routers/         # FastAPI router (batches, withdrawals, health)
│   │   └── tasks/               # Celery async tasks
│   ├── tests/                   # Bộ kiểm thử dịch vụ import-service
│   │   ├── test_wp02_suite.py   # Bộ kiểm thử tích hợp 8 tiêu chí
│   │   ├── test_wp02_extended.py# Kiểm thử mở rộng (quarantine, PII, backup)
│   │   ├── test_ops01_benchmark.py # Bài kiểm tra hiệu năng 500 dòng (OPS 01)
│   │   └── test_health.py
│   └── cli.py                   # Công cụ dòng lệnh CLI cho kỹ sư S2
├── import_cli.py                # Wrapper CLI tại thư mục gốc
└── README_WP02.md
```

---

## 2. Bảng Ánh Xạ Mã Yêu Cầu RFP Đã Triển Khai

| Mã Yêu Cầu | Hạng mục thực hiện trong code | Trạng thái |
| :--- | :--- | :---: |
| **WP02** | Xây dựng trọn bộ 2 CSV Validator, Manifest, Quarantine, Snapshot age | **ĐÁP ỨNG** |
| **DAT 01** | Lưu trữ Document ID, Passage ID, xuất xứ, người duyệt, phiên bản, thời gian hiệu lực | **ĐÁP ỨNG** |
| **DAT 02** | Cơ chế Reconcile dòng (`MATCH/MISMATCH`), Idempotent retry qua SHA-256, Tombstone xóa an toàn, bảo vệ không cho late batch ghi đè version mới | **ĐÁP ỨNG** |
| **DAT 06** | Validator ép kiểu chặt chẽ cho `critical_fields` (toán tử, đơn vị, ngưỡng, vai trò) | **ĐÁP ỨNG** |
| **DAT 07** | Triển khai `CRMContextValidator` cho Option O1, lọc allowlist nghiêm ngặt, chặn PII | **ĐÁP ỨNG** |
| **DAT 08** | Cách ly văn bản vượt quá 6.000 ký tự và bắt buộc đính kèm nội dung cước chú/bảng | **ĐÁP ỨNG** |
| **OPS 01** | Xử lý và đối soát 500 dòng trong **0.042 giây** (Cam kết RFP: $\le$ 30 phút) | **ĐÁP ỨNG** |
| **OPS 05 & SEC 05** | Kênh withdrawal tức thời: đổi trạng thái `withdrawn`, tạo tombstone, kích hoạt cache purge | **ĐÁP ỨNG** |
| **VN 01 & VN 03** | Hỗ trợ chuẩn tiếng Việt UTF-8 (có/không dấu), thuật ngữ kỹ thuật SongNhat | **ĐÁP ỨNG** |

---

## 3. Hướng Dẫn Sử Dụng Công Cụ CLI (`import_cli.py`)

### Nạp dữ liệu đoạn trích chính sách (`passages.csv`):
```bash
python import_cli.py import-passages data/sample/passages.csv --type snapshot
```

### Nạp bảng trường thông số ngưỡng (`critical_fields.csv`):
```bash
python import_cli.py import-critical-fields data/sample/critical_fields.csv --type snapshot
```

### Nạp ngữ cảnh CRM rút gọn (Option O1):
```bash
python import_cli.py import-crm data/sample/crm_context.csv --type snapshot
```

### Kiểm tra độ tươi của dữ liệu (Snapshot Age):
```bash
python import_cli.py snapshot-age
```

### Thu hồi chính sách khẩn cấp (Immediate Withdrawal):
```bash
python import_cli.py withdraw --type passage --id PAS-BG-01 --role PolicyOwner_P2 --reason "Thu hồi chính sách chiết khấu cũ"
```

---

## 4. Chạy Kiểm Thử Tự Động
```bash
# Chạy bộ test tích hợp toàn diện WP02 (8 tests)
python -m unittest import-service/tests/test_wp02_suite.py

# Chạy bộ test mở rộng (quarantine crit, O1 PII block, backup/restore)
python -m unittest import-service/tests/test_wp02_extended.py

# Chạy bài benchmark OPS 01 (500 dòng)
python -m unittest import-service/tests/test_ops01_benchmark.py
```

