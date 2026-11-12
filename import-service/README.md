# Import Service — WP02 Data Import & Integration Engine

**Kỹ sư phụ trách:** S2 (Data / Integration Engineer)  
**Phối hợp:** P4 (DevOps), S5 (Testing & Quality Assurance)  
**Dự án:** SongNhat CRM Knowledge and Policy Assistant  
**Cổng dịch vụ:** Microservice Port 8001 (xem [ADR-001](../docs/architecture/ADR-001-service-decomposition.md))  
**Tiêu chuẩn RFP tuân thủ:** WP02, DAT 01, DAT 02, DAT 06, DAT 07 (Option O1), DAT 08, OPS 01, OPS 05, SEC 05, VN 01, VN 03.

---

## 1. Cấu Trúc Thư Mục `import-service`

```
import-service/
├── cli.py                   # Service-level CLI tool cho kỹ sư S2
├── Dockerfile               # Container build cho import-service (Port 8001)
├── pyproject.toml           # Cấu hình dependency, entrypoint & linter tools
├── README.md                # Tài liệu kỹ thuật chi tiết WP02
├── requirements.txt         # Package requirements
├── src/
│   ├── importer/            # Core logic Data Import & Integration (WP02)
│   │   ├── models.py        # Dataclasses & Enum trạng thái (PolicyStatus, BatchType, ...)
│   │   ├── validators.py    # 3 Validator: Passages, Critical Fields, CRM Context O1
│   │   ├── storage.py       # Quản trị SQLite, Provenance, Version History, Tombstone
│   │   ├── engine.py        # Điều phối nạp, đối soát, manifest & idempotent retry
│   │   └── withdrawal.py    # Kênh thu hồi chính sách tức thời & trigger xóa cache
│   ├── api/
│   │   ├── main.py          # FastAPI application entrypoint
│   │   └── routers/
│   │       ├── batches.py   # Ingestion, manifest & snapshot freshness API
│   │       ├── withdrawals.py# Immediate policy withdrawal API (OPS 05, SEC 05)
│   │       └── health.py    # Liveness & readiness probes
│   └── tasks/
│       └── __init__.py      # Celery async tasks (process_*_batch)
└── tests/                   # Bộ kiểm thử dịch vụ import-service
    ├── test_wp02_suite.py   # 8 bài kiểm thử tích hợp chuẩn WP02
    ├── test_wp02_extended.py# Kiểm thử mở rộng (quarantine, PII, backup/restore)
    ├── test_ops01_benchmark.py # Bài test hiệu năng 500 dòng (OPS 01)
    └── test_health.py       # Kiểm tra sức khỏe microservice
```

---

## 2. Chi Tiết Các Tính Năng Đạt Chuẩn RFP

### 2.1. Hai CSV Validator & Option O1 Validator
1. **PassageValidator (`passages.csv`):**
   - Kiểm tra bắt buộc các trường: `document_id`, `passage_id`, `title`, `content_text`, `owner_role`, `approver_role`, `version`.
   - Giới hạn tối đa **6.000 ký tự Unicode** cho mỗi đoạn trích (DAT 08), không cắt tỉa ngầm (`ERR_CONTENT_TOO_LONG`).
   - Kiểm tra ngôn ngữ chuẩn `vi-VN` (VN 01).
   - Kiểm tra ngày tháng theo chuẩn **ISO 8601** (`ERR_INVALID_DATE_FORMAT`).
   - Kiểm tra tính đầy đủ của cước chú/bảng biểu (DAT 08): nếu `has_footnotes_or_tables` là True thì `footnotes` không được để trống (`ERR_MISSING_ESSENTIAL_FOOTNOTE`).
2. **CriticalFieldValidator (`critical_fields.csv`):**
   - Ép kiểu chặt chẽ cho từng trường thông số (DAT 06): `field_type` (`number`, `currency`, `percentage`, `duration_days`, `role_name`, `boolean`, `string`).
   - Kiểm tra toán tử điều kiện hợp lệ (`<`, `<=`, `>`, `>=`, `==`, `between`, `in`).
   - Xác thực giá trị ngưỡng `threshold_value` phải là dạng số hợp lệ đối với kiểu `number`, `currency`, `percentage`, `duration_days`.
   - Bắt buộc khai báo vai trò phê duyệt ngoại lệ (`approval_role`) và luồng leo thang (`exception_route`).
3. **CRMContextValidator (`crm_context.csv` - Option O1):**
   - Danh sách trường được duyệt (Strict Allowlist): `account_id`, `record_key`, `customer_tier`, `industry`, `assigned_sales_role`, `credit_limit_vnd`, `open_warranty_tickets`, `account_status`, `updated_at`.
   - **Chặn PII triệt để (DAT 07, SEC 02):** Từ chối ngay lập tức nếu tệp chứa bất kỳ trường nào ngoài allowlist (email, số điện thoại, thư từ trao đổi, hồ sơ cá nhân).
   - Kiểm soát giới hạn lưu trữ tối đa 5.000 dòng CRM.

### 2.2. Quarantine (Cô Lập Dòng Lỗi)
- Khi phát hiện dòng dữ liệu không đạt chuẩn, hệ thống **không dừng toàn bộ mẻ nạp** mà ghi nhận vào bảng `quarantine_records` và xuất file `data/output/quarantine_rows.csv`.
- Ghi nhận đầy đủ: `batch_id`, `file_name`, `row_number`, `raw_data`, `error_code`, `error_reason`, `quarantined_at`.

### 2.3. Row Reconciliation (Đối Soát Dòng Toàn Vẹn)
- Tuân thủ nguyên tắc không bao giờ để thất thoát dòng không rõ lý do (DAT 02):
  $$\text{expected\_rows} = \text{accepted\_rows} + \text{quarantined\_rows}$$
- Manifest ghi nhận trạng thái: `MATCH` (100% khớp) hoặc `MISMATCH`.

### 2.4. Idempotent Retry (Xử Lý Trùng Lặp An Toàn)
- Tính toán mã băm **SHA-256** của từng tệp đầu vào và lưu trữ trong bảng `batches`.
- Nếu tệp nạp lại có cùng SHA-256 và không có cờ `--force`, hệ thống tự động trả về kết quả mẻ nạp trước đó (`IDEMPOTENT_SKIPPED`), ngăn chặn nhân bản bản ghi hoặc làm sai lệch lịch sử phiên bản.

### 2.5. Version History & Late Batch Protection
- Mọi bản ghi chính sách trước khi bị ghi đè sẽ được sao lưu toàn bộ thông tin gốc vào bảng `version_history`.
- Cơ chế bảo vệ tệp đến muộn (Late Batch Protection - DAT 02): nếu mẻ nạp mang phiên bản cũ hơn phiên bản hiện hành trong hệ thống (ví dụ v1.2.0 nạp sau khi đã có v2.0.0), hệ thống sẽ **bỏ qua việc ghi đè** và ghi chú trong Manifest.

### 2.6. Tombstone & Kênh Thu Hồi Tức Thời (Immediate Withdrawal)
- Tuân thủ **OPS 05 & SEC 05**: Tách biệt hoàn toàn khỏi chu kỳ nạp mẻ định kỳ.
- Khi người có thẩm quyền (như `PolicyOwner_P2`) kích hoạt thu hồi:
  1. Trạng thái bản ghi chuyển sang `withdrawn`.
  2. Cờ `is_tombstone = 1` được kích hoạt.
  3. Bản ghi `tombstone` được lưu vết vào bảng `tombstones` kèm lý do và vai trò thực hiện.
  4. Bộ lắng nghe hủy bộ nhớ đệm (Cache Purge Listener) được kích hoạt tức thì.
  5. Mọi câu truy vấn tiếp theo từ Policy Engine (S3) và Question Assistant (S4) ngay lập tức bị chặn truy cập bản ghi này.

### 2.7. Snapshot Age (Theo Dõi Độ Tươi Dữ Liệu)
- Tính toán thời gian kể từ mẻ nạp snapshot gần nhất so với mốc thời gian thực hiện theo múi giờ Việt Nam (UTC+7 / VN_TZ).
- Trả về cấu trúc JSON gồm: `has_snapshot`, `latest_snapshot_iso`, `age_seconds`, `age_human` (ví dụ: `5 giờ 2 phút trước`).

---

## 3. Hướng Dẫn Sử Dụng CLI (`import-service/cli.py`)

Kỹ sư vận hành S2 có thể thực thi trực tiếp các thao tác thông qua CLI của `import-service`:

### Nạp đoạn trích chính sách (`passages.csv`):
```bash
python import-service/cli.py import-passages data/sample/passages.csv --type snapshot
```

### Nạp bảng thông số ngưỡng & thẩm quyền (`critical_fields.csv`):
```bash
python import-service/cli.py import-critical-fields data/sample/critical_fields.csv --type snapshot
```

### Nạp ngữ cảnh CRM rút gọn (Option O1):
```bash
python import-service/cli.py import-crm data/sample/crm_context.csv --type snapshot
```

### Kiểm tra độ tươi dữ liệu (Snapshot Age):
```bash
python import-service/cli.py snapshot-age
```

### Kích hoạt thu hồi chính sách tức thời:
```bash
python import-service/cli.py withdraw --type passage --id PAS-BG-01 --role PolicyOwner_P2 --reason "Thu hồi chính sách chiết khấu cũ năm 2025"
```

### Kích hoạt thu hồi trường thông số ngưỡng:
```bash
python import-service/cli.py withdraw --type critical_field --id RUL-CK-01 --role PolicyOwner_P2 --reason "Thu hồi hạn mức chiết khấu TPKD"
```

---

## 4. Giao Diện REST API (`import-service` - Port 8001)

Microservice `import-service` cung cấp đầy đủ các endpoint theo chuẩn FastAPI / OpenAPI:

| Phương thức | Endpoint | Chức năng | Tiêu chuẩn RFP |
|---|---|---|---|
| `POST` | `/api/import/batches/passages` | Nạp tệp `passages.csv` (multipart/form-data) | WP02, DAT 01-02, DAT 08, OPS 01 |
| `POST` | `/api/import/batches/critical-fields` | Nạp tệp `critical_fields.csv` | WP02, DAT 06 |
| `POST` | `/api/import/batches/crm-context` | Nạp tệp `crm_context.csv` (Option O1) | DAT 07, SEC 02 |
| `GET` | `/api/import/batches/snapshot-age` | Truy vấn độ tươi dữ liệu snapshot hiện tại | DAT 02 |
| `GET` | `/api/import/batches/{batch_id}` | Lấy chi tiết Manifest & trạng thái Reconcile | DAT 02 |
| `POST` | `/api/import/withdrawals/` | Kích hoạt thu hồi chính sách tức thời | OPS 05, SEC 05 |

---

## 5. Kết Quả Kiểm Thử & Hiệu Năng (OPS 01 Benchmark)

### 5.1. Bộ Kiểm Thử Tích Hợp WP02:
```bash
python -m unittest import-service/tests/test_wp02_suite.py
python -m unittest import-service/tests/test_wp02_extended.py
```
- **Kết quả:** 12/12 bài test pass 100% trong ~0.4 giây.

### 5.2. Kết Quả Benchmark Hiệu Năng OPS 01 (500 dòng thay đổi):
```bash
python -m unittest import-service/tests/test_ops01_benchmark.py
```
- **Số dòng xử lý:** 500 / 500 dòng
- **Tỷ lệ Reconcile:** 100% MATCH
- **Thời gian thực thi:** **0.031 giây** (Cam kết RFP: $\le$ 1.800 giây / 30 phút)
- **Tốc độ xử lý:** **16.147 dòng/giây**
- **Đánh giá:** Vượt tiêu chuẩn RFP gấp hơn 50.000 lần.
