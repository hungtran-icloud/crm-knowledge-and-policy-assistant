# Kiến trúc tổng thể — SongNhat CRM Knowledge & Policy Assistant

> Xem chi tiết trong tài liệu `songnhat_architecture_overview.md` (đề xuất kiến trúc nội bộ).

## Lựa chọn kiến trúc

**Modular Monolith + RAG + Policy Control Layer**

## Các module backend

| Module | Trách nhiệm |
|---|---|
| `identity` | Đăng nhập, xác thực, phân quyền RBAC |
| `knowledge` | Quản lý tài liệu, phiên bản, passage, metadata |
| `ingestion` | Import CSV, validate, manifest, quarantine, reconciliation |
| `policy` | Phiên bản, thẩm quyền, trạng thái, effective dates, phạm vi |
| `retrieval` | Semantic search (pgvector), từ khóa, lọc bằng chứng |
| `answer` | Điều phối RAG: applicability → retrieval → LLM → validation |
| `validation` | Kiểm tra citation, critical fields, tính đầy đủ |
| `referral` | Chuyển Policy Owner khi thiếu căn cứ |
| `feedback` | Ghi nhận phản hồi, đề xuất chỉnh sửa |
| `audit` | Lịch sử truy cập, truy vấn, thay đổi |
| `evaluation` | Bộ test, đo chất lượng retrieval/answer |
| `admin` | Quản trị người dùng, cấu hình |

## Luồng hỏi đáp

```
Staff question
  → Authenticate & Authorize (identity)
  → Intent & date/scope detection
  → Policy Applicability Engine (policy)
  → Permission check (identity)
  → Evidence Retrieval (retrieval — pgvector + FTS)
  → Critical Field Resolver (policy)
  → LLM Answer Generation (answer)
  → Citation & Claim Validation (validation)
  → Final permission & source-state check
  → Display Answer Package (UI)
```

## Nguyên tắc quan trọng

- Business logic (quyền, hiệu lực, phạm vi) xử lý ở backend — không giao cho LLM.
- Không hiển thị câu trả lời trước khi hoàn tất validation.
- Fail closed: khi trạng thái thẩm quyền không khả dụng, không trả nội dung bị ảnh hưởng.
- Citation phải lưu: document_id, version_id, passage_id, page_number, quoted_text.

## Các giai đoạn triển khai

| Giai đoạn | Module cần hoàn thành |
|---|---|
| 1. Foundation | identity, knowledge, ingestion, policy version |
| 2. Retrieval | retrieval, applicability, critical field |
| 3. Answering | answer, validation, chat UI |
| 4. Governance | referral, feedback, audit |
| 5. Assurance | evaluation, monitoring, security |
