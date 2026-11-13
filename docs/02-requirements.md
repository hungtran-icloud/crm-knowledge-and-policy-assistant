# 02. Requirements – Phân tích yêu cầu

> **Phiên bản:** 0.1 – Draft for validation  
> **Nguồn chuẩn:** SongNhat CRM Knowledge and Policy RFP.  
> **Quy ước:** `M` = mandatory trong base scope; `O` = option/ngoài base scope; `TBC` = cần xác nhận tại G0.

## 1. Business Requirements

| ID | Yêu cầu | M/O | Tiêu chí kiểm tra |
|---|---|---:|---|
| BR-01 | Giảm việc tìm kiếm lặp lại và giải thích quy trình thiếu nhất quán | M | Có baseline và đo effort trong pilot |
| BR-02 | Nhân viên xác định đúng policy/version/scope/ngày áp dụng | M | Đánh giá trên sealed answerable tasks |
| BR-03 | Hiển thị điều khoản và nguồn gốc để nhân viên tự kiểm tra | M | Mỗi material claim có citation áp dụng |
| BR-04 | Policy Owner giữ quyền phê duyệt và duy trì nội dung | M | Có owner, approver, publication workflow |
| BR-05 | Quản lý thay đổi, scheduled effectiveness, withdrawal và impact | M | Kiểm thử thay đổi và thu hồi |
| BR-06 | So sánh lợi ích với tổng chi phí và effort duy trì | M | Báo cáo G3 có cost/use/effort |
| BR-07 | Selected CRM context cho một record được chọn | O1 | Chỉ bật sau khi có phê duyệt riêng |

## 2. Functional Requirements

### 2.1 Knowledge & Import

| ID | Yêu cầu | Priority |
|---|---|---|
| FR-KB-01 | Import approved passages qua schema CSV UTF-8 | Must |
| FR-KB-02 | Import critical policy fields qua schema CSV UTF-8 | Must |
| FR-KB-03 | Lưu stable document/passage IDs, title, original reference, section/page, language | Must |
| FR-KB-04 | Lưu owner, approver, version, recorded/publication time, effective interval, scope, audience | Must |
| FR-KB-05 | Phân biệt full snapshot và increment; reconciliation accepted/quarantined rows | Must |
| FR-KB-06 | Retry idempotent; batch đến muộn không ghi đè version mới | Must |
| FR-KB-07 | Hỗ trợ tombstone/approved snapshot để xử lý xóa; không suy luận xóa từ row vắng mặt | Must |
| FR-KB-08 | Quarantine nội dung thiếu, quá lớn, không đọc được hoặc thiếu footnote thiết yếu | Must |
| FR-KB-09 | Withdrawal có hiệu lực theo control được ủy quyền, không đợi batch kế tiếp | Must |

### 2.2 Authority, Version & Applicability

| ID | Yêu cầu | Priority |
|---|---|---|
| FR-POL-01 | Authority matrix theo từng policy family | Must |
| FR-POL-02 | Phân biệt policy, SOP, manufacturer terms, customer contract và staff notes | Must |
| FR-POL-03 | Chọn governing date và scope theo company/branch/role/customer category/product/transaction | Must |
| FR-POL-04 | Không tự suy luận thứ tự ưu tiên giữa contract và company policy | Must |
| FR-POL-05 | Hold kết luận khi phiên bản chồng lấn, conflict hoặc thiếu quy tắc ngày | Must |
| FR-POL-06 | Critical fields có kiểu dữ liệu, operator, currency/unit, role, deadline, exception và clause liên kết | Must |
| FR-POL-07 | Giá trị/điều kiện critical được render từ dữ liệu đã duyệt, không để model prose tự sửa | Must |

### 2.3 Question Answering & Workspace

| ID | Yêu cầu | Priority |
|---|---|---|
| FR-ANS-01 | Hỗ trợ câu hỏi về cách hoàn thành CRM task, rule áp dụng, thông tin thiếu và tuyến review ngoại lệ | Must |
| FR-ANS-02 | Tìm kiếm tiếng Việt, hỗ trợ approved synonyms, thiếu dấu và thuật ngữ hỗn hợp | Must |
| FR-ANS-03 | Lọc quyền, publication state, effective date và scope trước khi hiển thị evidence | Must |
| FR-ANS-04 | Answer package hiển thị question, governing date, scope, guidance, citations, fields, missing facts, referral | Must |
| FR-ANS-05 | Mỗi material claim có exact applicable clause citation và version | Must |
| FR-ANS-06 | Phân biệt quoted rule text với explanatory wording | Must |
| FR-ANS-07 | Hỏi clarification khi thiếu dữ kiện thiết yếu | Must |
| FR-ANS-08 | Hold khi thiếu nguồn, xung đột hoặc thiếu footnote/table/diagram quan trọng | Must |
| FR-ANS-09 | Hiển thị uncertainty và lý do không thể kết luận | Must |
| FR-ANS-10 | Không stream nội dung chưa qua final source/permission check | Must |

### 2.4 Referral, Feedback & Change

| ID | Yêu cầu | Priority |
|---|---|---|
| FR-OPS-01 | Tạo local referral record với context tối thiểu và unresolved issue | Must |
| FR-OPS-02 | Theo dõi referral, owner response recorded và closure riêng biệt | Must |
| FR-OPS-03 | User correction/owner response chỉ là knowledge candidate | Must |
| FR-OPS-04 | Chỉ xuất bản sau review, approval, versioning và effective date | Must |
| FR-OPS-05 | Phân loại feedback: missing source, obsolete rule, wrong scope, omitted exception, rejection | Must |
| FR-OPS-06 | Khi source/access thay đổi, đánh dấu answer cũ stale và yêu cầu truy vấn mới | Must |
| FR-OPS-07 | Không tự động train hoặc tự thay đổi policy từ feedback | Must |

### 2.5 Security & Administration

| ID | Yêu cầu | Priority |
|---|---|---|
| FR-SEC-01 | RBAC cho reader, policy owner/publisher, steward và administrator | Must |
| FR-SEC-02 | Quyền nguồn được kiểm tra trước retrieval và display | Must |
| FR-SEC-03 | Audit actor, time, source/version, question, answer, holds và referral theo mục đích được duyệt | Must |
| FR-SEC-04 | Nội dung import và câu hỏi được xem là untrusted data, không phải system instruction | Must |
| FR-SEC-05 | Không cung cấp unrestricted tools, public web retrieval hoặc credentials trong prompt | Must |
| FR-SEC-06 | O1 CRM context phải có identity, permissions, lawful processing, allowlist và freshness check | O1 |

## 3. Non-functional Requirements

Các số dưới đây là mục tiêu/giả định RFP để kiểm thử trong môi trường thực tế, không phải kết quả hiện tại.

| ID | Nhóm | Yêu cầu |
|---|---|---|
| NFR-01 | Language | Unicode tiếng Việt; test thiếu dấu, viết tắt CRM, thuật ngữ Anh, negation, date, amount, unit |
| NFR-02 | Import performance | Xử lý 500 changed rows trong 30 phút và reconcile từng row |
| NFR-03 | Response performance | Với 5 concurrent users, target p95 ≤25 giây trên 100 requests trong context caps |
| NFR-04 | Availability | RFP đề xuất 99.5% trong contracted service hours; cần chốt hợp đồng |
| NFR-05 | Recovery | RTO mục tiêu 4 covered hours; RPO 24 hours |
| NFR-06 | Security | Zero observed unauthorized disclosure; critical access/withdrawal tests pass |
| NFR-07 | Grounding | Zero fabricated citations; material claims có căn cứ |
| NFR-08 | Reliability | Không dùng withdrawn/future/draft policy làm current guidance |
| NFR-09 | Auditability | Có thể truy vết câu trả lời về nguồn, version, scope, date và actor |
| NFR-10 | Portability | Export permitted records, versions, references, mappings và audit ở open formats |
| NFR-11 | Cost controls | Có usage/cost meters, caps, hold khi vượt hạn mức; không silent truncation |
| NFR-12 | Privacy | Review actual processing, providers, retention, transfers và legal applicability trước dữ liệu thật |

## 4. User Stories

- **US-01 – Tra cứu quy trình:** Là nhân viên, tôi muốn hỏi cách hoàn thành một CRM task để biết các bước và thông tin cần chuẩn bị.
- **US-02 – Xác định policy:** Là nhân viên, tôi muốn biết policy/version áp dụng theo ngày và phạm vi giao dịch.
- **US-03 – Kiểm tra căn cứ:** Là nhân viên, tôi muốn mở đúng điều khoản và nguồn gốc để tự xác minh.
- **US-04 – Thiếu dữ kiện:** Là nhân viên, tôi muốn hệ thống hỏi rõ thông tin còn thiếu thay vì đoán.
- **US-05 – Referral:** Là nhân viên, tôi muốn biết Policy Owner hoặc tuyến xử lý khi có conflict/exception.
- **US-06 – Quản lý policy:** Là Policy Owner, tôi muốn review, approve, schedule, supersede và withdraw policy.
- **US-07 – Import:** Là Steward, tôi muốn import dữ liệu và nhận reconciliation/quarantine report.
- **US-08 – Kiểm toán:** Là Privacy/Security Owner, tôi muốn kiểm tra ai truy cập nguồn và câu trả lời nào đã được tạo.
- **US-09 – Đánh giá:** Là QA/Reviewer, tôi muốn chạy sealed tests độc lập để đánh giá chất lượng.
- **US-10 – Vận hành:** Là Admin, tôi muốn backup/restore và export dữ liệu theo quy trình đã duyệt.

## 5. Use Cases

| UC | Actor | Luồng chính | Ngoại lệ/hold |
|---|---|---|---|
| UC-01 General policy question | Staff | Nhập câu hỏi → hệ thống lọc quyền/scope/date → retrieve → trả lời và citations | Không có nguồn phù hợp → hỏi rõ hoặc referral |
| UC-02 Dated transaction | Staff | Cung cấp ngày sự kiện → áp dụng governing-date rule đã duyệt → hiển thị version lịch sử | Thiếu date rule → hold |
| UC-03 Commercial exception | Staff | Hỏi tuyến xin ngoại lệ → hiển thị điều kiện và evidence cần có | Không tự cấp approval |
| UC-04 Conflicting sources | Staff/Owner | Phát hiện conflict → hiển thị evidence được phép → referral | Không tự chọn precedence |
| UC-05 Publish policy | Owner/Publisher | Review metadata/content → approve → schedule/effective | Thiếu quyền/approval → không publish |
| UC-06 Withdraw policy | Authorized owner | Commit withdrawal/access change → block future retrieval/reuse → mark old answers stale | Đã hiển thị/copy trước đó không thể thu hồi chắc chắn |
| UC-07 Import corpus | Steward | Validate → reconcile → accept/quarantine → audit | Duplicate/late/partial data xử lý theo contract |
| UC-08 Feedback | Staff/Owner | Gửi correction → phân loại candidate → owner review | Không tự động thay đổi knowledge |

## 6. Acceptance Criteria

### 6.1 Critical controls – Zero tolerance

- Zero observed unauthorized disclosure.
- Zero fabricated critical field.
- Zero false approval.
- Zero current guidance dựa trên withdrawn/future policy.
- Tất cả critical access, withdrawal và critical field challenge tests pass.
- Bất kỳ critical failure nào đều block release.

### 6.2 Chỉ tiêu sealed evaluation

| Tiêu chí | Mục tiêu RFP |
|---|---:|
| Correct version/scope/governing date | ≥95% |
| Material claims supported by applicable clauses | ≥95% |
| Required clauses/exceptions included | ≥90% |
| Fabricated citations | 0 |
| Retrieval recall@5 | ≥90% |
| Answerable tasks useful with minor edits | ≥80% |
| Unanswerable tasks with materially unsupported answers | ≤5% |

### 6.3 Pilot

- Tối thiểu 20 business days supervised use.
- Mục tiêu giảm 20% mean total staff effort với audited quality bằng hoặc tốt hơn.
- Đếm cả preparation, checking, failed attempts, correction và fallback.
- G3 cần effort/use/cost report; quyết định mở rộng là quyết định riêng.

### 6.4 Evaluation dataset

RFP đề xuất:
- 200 permitted real question tasks: 60 development, 40 validation, 100 sealed acceptance.
- 80 constructed challenges.
- Hai Policy Reviewers thống nhất labels về clause/date/scope/exception/referral.
- Developer không được tune trên sealed cases.
- Nếu lộ sealed cases, cần fresh independent retest.

## 7. Constraints & Assumptions

- 2 tuần capped Discovery, sau G0 là 10 tuần base implementation theo RFP.
- Không nén 20 business days supervised observation.
- Base scope không nhập customer records.
- Hai base CSV schemas; O1 là schema thứ ba và phải được duyệt/định giá riêng.
- Các volume caps, user counts và data ceilings là bid assumptions cần xác nhận G0.
- Không có vendor/model/workflow engine cụ thể bắt buộc.
- Phải so sánh searchable library, configured product và bounded custom build.
- Không tự giả định model fine-tuning là bắt buộc.
- Legal/privacy/security applicability phải được owner có thẩm quyền đánh giá trước G2.

## 8. Traceability

Mỗi requirement cần liên kết:
`Requirement ID → Jira Issue → Design/ADR → Test Case → Evidence → Release Gate`.

## 9. Source Notes

RFP trang 3–8 (scope, data/answer requirements), trang 9–10 (evaluation/acceptance), trang 10–12 (gates, schedule, ownership), trang 20–22 và 28 (worked cases, operations, Vietnam fixtures).
