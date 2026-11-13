# TEAM PLAYBOOK
> **ĐỌC KỸ TRƯỚC KHI BẮT ĐẦU CODE. ĐÂY LÀ QUY TRÌNH BẮT BUỘC CHO TOÀN NHÓM.**  
> **Dự án:** SongNhat CRM Knowledge & Policy Assistant  
> **Phiên bản:** 1.0 – Team Working Agreement  
> **Phạm vi:** Tất cả thành viên tham gia phân tích, phát triển, kiểm thử, vận hành và quản lý dự án.

## 0. Cam kết chung

Khi tham gia dự án, mỗi thành viên có trách nhiệm:
- Đọc tài liệu này cùng Jira Rules, GitHub Rules và các tài liệu dự án liên quan.
- Tuân thủ quy trình Jira → Branch → Code/Test → Pull Request → Review → Merge → Verify → cập nhật Jira.
- Không tự ý thay đổi scope, policy, quyền truy cập, tiêu chí nghiệm thu hoặc kiến trúc đã được chốt.
- Chủ động báo blocker; không im lặng khi trễ hoặc không hiểu yêu cầu.
- Không đưa dữ liệu, secrets hoặc tài liệu không được phép vào công cụ/code/test.
- Tôn trọng vai trò phê duyệt của Business/Policy Owner và người nghiệm thu độc lập.

**Không bắt đầu code khi Issue chưa đạt Definition of Ready.**

## 1. Dự án đang xây dựng gì?

SongNhat CRM Knowledge & Policy Assistant là trợ lý tra cứu tri thức và chính sách nội bộ. Hệ thống hỗ trợ nhân viên tìm kiếm hướng dẫn đã được phê duyệt, xác định policy phù hợp theo phạm vi và ngày áp dụng, trình bày clause/citation chính xác, hiển thị các trường quan trọng, nêu thông tin còn thiếu và chuyển câu hỏi tới đúng owner khi cần.

### 1.1 Nguyên tắc sản phẩm không được vi phạm

1. **Evidence trước, answer sau:** Chỉ tạo câu trả lời hoàn chỉnh sau khi đã kiểm tra nguồn, phiên bản, quyền, trạng thái publication, effective date và scope.
2. **Authority thuộc con người:** Policy Owner và hệ thống có thẩm quyền giữ quyền quyết định/phê duyệt/thực thi. Assistant không phê duyệt giao dịch, không thay thế chuyên gia hoặc người có thẩm quyền.
3. **Citation phải kiểm chứng được:** Claim trọng yếu phải trỏ tới clause/nguồn/phiên bản áp dụng. Không bịa citation.
4. **Không chắc thì hold/referral:** Thiếu dữ kiện, xung đột, nguồn lỗi hoặc quyền không rõ thì nêu rõ lý do và chuyển owner; không đoán.
5. **Policy có thời gian và trạng thái:** Phải phân biệt draft, approved, published, scheduled, effective, superseded và withdrawn theo mô hình trạng thái đã được chốt.
6. **Không tự sửa policy:** Feedback hoặc câu hỏi không tự động làm thay đổi rule, dữ liệu chuẩn hay model.
7. **Tách dữ liệu khỏi suy luận:** Critical fields phải lấy từ nguồn/logic xác định, không lấy giá trị model tự sinh làm sự thật.

### 1.2 Base scope và ranh giới dữ liệu

- Base scope dùng approved procedures/clauses và structured critical fields; **không nhập customer records**.
- Option O1 (selected CRM context) là phạm vi riêng, chỉ xem xét khi identity, reader permissions, lawful processing, freshness và incremental value đã được xác minh/phê duyệt.
- Không tự thêm mailbox history, full customer dossiers, live connectors, workflow automation, OCR hoặc transaction execution vào base scope.
- Không dùng dữ liệu thật trong prompt, log, fixture, screenshot hoặc issue nếu chưa có quyền và quy trình bảo vệ được duyệt.

## 2. Tài liệu phải đọc trước khi code

Theo thứ tự:

1. `01-project-overview.md` – mục tiêu, scope và out of scope.
2. `02-requirements.md` – business/functional/non-functional requirements và acceptance.
3. `03-project-planning.md` – timeline, G0–G4, Sprint, risks và change control.
4. `04-team-responsibilities.md` – vai trò và quyền quyết định.
5. `05-technical-design.md` – kiến trúc, stack, API, database.
6. `06-development-standards.md` – coding, naming, structure, DoD.
7. `07-project-management-tools.md` – công cụ và nguồn sự thật.
8. `08-quality-assurance-testing.md` – test strategy và acceptance.
9. `09-security-deployment.md` – security, environments, deployment.
10. `10-documentation-index.md` – tài liệu bàn giao.
11. `11-jira-working-rules.md` – cách tạo/cập nhật Issue.
12. `12-github-working-rules.md` – branch, commit, PR, review, merge.
13. Tài liệu/ADR/Issue cụ thể gắn với công việc được giao.

Nếu tài liệu mâu thuẫn:
- Không tự chọn cách hiểu có lợi cho việc code nhanh.
- Ghi câu hỏi/decision vào Jira, nêu tác động.
- BA/PM xử lý nghiệp vụ và scope; Tech Lead xử lý kỹ thuật; Policy Owner xử lý nội dung/authority; Security/Privacy Owner xử lý quyền và dữ liệu.
- Quyết định có ảnh hưởng kiến trúc phải ghi ADR; thay đổi scope phải qua change control.

## 3. Nguồn sự thật và công cụ

| Nội dung | Nguồn sự thật |
|---|---|
| Yêu cầu, owner, priority, tiến độ, Sprint, blocker | Jira |
| Source code, branch, commit, PR, review, CI | GitHub |
| Quy tắc nghiệp vụ/policy được áp dụng | Nguồn chính sách đã được Policy Owner phê duyệt |
| Kiến trúc và quyết định kỹ thuật | Technical Design + ADR |
| Thiết kế UI/UX | Figma hoặc tài liệu thiết kế được nhóm chọn |
| Trao đổi nhanh | Kênh chat của nhóm; quyết định phải được ghi lại đúng nơi |

Tin nhắn chat không thay thế Jira Issue, PR review hoặc phê duyệt policy.

## 4. Quy trình bắt buộc trước khi code

### Bước 1 – Nhận việc qua Jira
- Tìm Issue được giao; đọc Epic, Description, AC, priority, Gate, dependency và tài liệu liên quan.
- Xác nhận Assignee và Sprint.
- Nếu Issue thiếu thông tin, chuyển về cần làm rõ hoặc comment câu hỏi; không tự suy diễn.
- Xác định dữ liệu/nguồn cần dùng có được phép hay không.

### Bước 2 – Xác nhận Definition of Ready

Chỉ bắt đầu khi tất cả điều kiện áp dụng đều đạt:

- [ ] Mục tiêu và phạm vi rõ.
- [ ] Acceptance Criteria kiểm chứng được.
- [ ] Priority và Release Gate đã xác định.
- [ ] Có owner và dependency.
- [ ] Nguồn/tài liệu/test data được phép truy cập.
- [ ] Biết cách kiểm thử và bằng chứng cần nộp.
- [ ] Không có quyết định blocking chưa được giải quyết.

### Bước 3 – Thiết kế trước thay đổi
- Kiểm tra code hiện có, convention, API/schema và test liên quan.
- Xác định component/module bị ảnh hưởng.
- Xác định tác động đến database, permission, policy date/version, citations, logs, cache và deployment.
- Nếu quyết định ảnh hưởng cấu trúc hệ thống, chọn dependency lớn, thay đổi data model hoặc thay đổi integration boundary, tạo ADR/đề nghị Tech Lead duyệt trước.
- Với thay đổi nghiệp vụ/policy, phải có nguồn và Policy Owner rõ ràng.

### Bước 4 – Tạo branch
- Tạo branch từ base branch mới nhất.
- Dùng tên theo format trong GitHub Rules: `feature/SON-123-short-description`, `fix/...`, `docs/...`, v.v.
- Không code trực tiếp trên `main`.
- Một branch tập trung một Issue/mục tiêu liên quan.

### Bước 5 – Code và kiểm thử
- Tuân thủ Development Standards.
- Viết test cùng lúc với code, không để toàn bộ test đến cuối Sprint.
- Test cả happy path, negative path, boundary, permission và failure cases liên quan.
- Không hard-code policy rules hoặc critical values nếu chúng phải được quản lý bằng dữ liệu/metadata có thẩm quyền.
- Không dùng LLM để quyết định quyền, effective date, publication state hoặc critical fields.
- Không log dữ liệu nhạy cảm.
- Cập nhật docs/schema/migration/ADR nếu thay đổi làm tài liệu cũ không còn đúng.

### Bước 6 – Tạo PR và review
- PR phải có Jira Key, mục tiêu, scope, cách test, kết quả test, rủi ro và evidence.
- Tác giả không tự approve.
- Chờ reviewer độc lập và CI pass.
- Sửa comment blocking; không merge khi còn vấn đề critical.
- Thay đổi policy/security/data phải có reviewer phù hợp.

### Bước 7 – Merge và verify
- Merge theo branch protection.
- Kiểm tra CI/deployment nếu có.
- Chạy test xác nhận sau merge theo yêu cầu.
- Cập nhật Jira bằng PR link, test evidence, kết quả và trạng thái thực tế.
- Chỉ Done khi DoD đạt.

## 5. Roadmap và Release Gates

RFP quy định **5 Release Gates G0–G4**. Sprint là cách tổ chức công việc nội bộ; không đồng nhất một-một với Gate.

| Gate | Mục tiêu | Điều kiện trọng yếu |
|---|---|---|
| G0 – Ready to build | Sẵn sàng triển khai | Chốt policy families, sample được duyệt, curation capacity, rights, authority, recurring tasks và so sánh route/chi phí |
| G1 – Controlled offline | Corpus và kiểm soát dữ liệu đúng | Approved corpus/field rows; import reconcile; permissions, effective dates, conflicts và original references được xác minh |
| G2 – Supervised use | Sẵn sàng đưa vào sử dụng có giám sát | Independent quality/challenge gates pass; không critical defect; legal deployment review hoàn tất; owners được training; fallback sẵn sàng |
| G3 – Pilot acceptance | Chấp nhận pilot theo kết quả đo | Tối thiểu 20 business days supervised use; báo cáo effort/use/cost; quyết định mở rộng tách biệt |
| G4 – Handover | Bàn giao có thể vận hành/thoát | Code, schemas, mappings, config, docs, training, restore/exit tests và dữ liệu portable theo quyền |

### 5.1 Các ngưỡng acceptance quan trọng từ RFP

Các ngưỡng dưới đây là yêu cầu nghiệm thu RFP, không phải chỉ số tùy chọn:

- Zero observed unauthorized disclosure, fabricated critical field, false approval hoặc dùng current guidance từ policy withdrawn/future.
- Tất cả critical challenge tests phải pass.
- ≥95% đúng version/scope/governing date trên sealed answerable tasks.
- ≥95% material claims được hỗ trợ bởi applicable clauses; ≥90% required clauses/exceptions được đưa vào; zero fabricated citations.
- ≥90% retrieval recall@5 trên sealed subset có approved applicable evidence.
- ≥80% answerable tasks tạo được câu trả lời hữu ích với minor edits; ≤5% unanswerable tasks nhận câu trả lời materially unsupported.
- Pilot supervised tối thiểu 20 ngày làm việc; mục tiêu giảm 20% mean total staff effort với audited quality bằng hoặc tốt hơn.

RFP nêu bộ test dự kiến gồm 200 permitted real question tasks (60 development, 40 validation, 100 sealed acceptance) và 80 constructed challenges. Developer không được tune trên sealed cases. Nếu lộ sealed cases, cần fresh independent retest.

Không thay đổi mẫu số, ngưỡng hoặc định nghĩa đo sau khi thấy kết quả nếu chưa có quyết định chính thức và ghi rõ lý do.

## 6. Sprint và nhịp làm việc

### 6.1 Sprint planning
- Sprint Goal phải gắn với một kết quả có thể demo/đánh giá.
- Chỉ đưa Issue đạt DoR vào Sprint.
- Xem xét Gate, dependency, risk, capacity và test effort.
- Mỗi Issue có một Assignee chính.
- Không cam kết quá capacity.

### 6.2 Daily sync mỗi 2 ngày
Thời lượng đề xuất: 15–20 phút. Trước buổi họp, mọi người cập nhật Jira.

Mỗi người trả lời theo Issue Key:
1. **What did you do?** – Đã làm gì kể từ lần sync trước?
2. **What are you doing?** – Đang làm Issue nào?
3. **What will you do next?** – Bước tiếp theo?
4. **Do you need help?** – Có blocker/cần hỗ trợ?
5. **Any other questions?** – Có câu hỏi/quyết định nào cần làm rõ?

Quy tắc họp:
- Nói ngắn, đúng trọng tâm, có Jira Key.
- Không báo cáo chung chung “đang code”.
- Blocker phải có người hỗ trợ và thời điểm cập nhật.
- Debug sâu chuyển sang buổi kỹ thuật riêng.
- Không dùng daily để truy lỗi cá nhân; mục tiêu là đồng bộ và gỡ vướng.

### 6.3 Review và retrospective
- Demo theo AC, không demo chỉ bằng lời.
- Nêu rõ phần hoàn thành, phần chưa hoàn thành và rủi ro.
- Retrospective tập trung vào quy trình, nguyên nhân hệ thống và hành động cải tiến.
- Action cần theo dõi phải tạo Jira Issue có owner và due date phù hợp.

## 7. Quy tắc kỹ thuật chung

### 7.1 Kiến trúc và stack
Baseline hiện tại trong tài liệu dự án là **Modular Monolith** theo hướng API-first, Python/FastAPI cho backend, RAG cho retrieval/answering, PostgreSQL (có thể dùng pgvector), frontend React/Next.js và Docker cho môi trường đóng gói. Đây là baseline đề xuất của nhóm, không phải lựa chọn vendor/model được RFP bắt buộc.

Mọi thay đổi stack/framework/model/vector store phải:
- Có lý do kỹ thuật và so sánh trade-off.
- Đánh giá chi phí, privacy, provider location, retention, sub-processors và vận hành.
- Có benchmark trên tác vụ tiếng Việt và corpus được phép.
- Được Tech Lead chấp thuận; quyết định quan trọng ghi ADR.

### 7.2 “Chuẩn bị trước, trả lời sau”
Hiểu là chuẩn bị dữ liệu và evidence trước khi sinh câu trả lời:
1. Kiểm tra quyền và nguồn.
2. Chuẩn hóa/curate tài liệu, metadata và critical fields.
3. Quản lý version, authority, publication state, effective date, scope.
4. Import và reconciliation.
5. Index/search và retrieval.
6. Đánh giá trên validation set.
7. Chỉ sau final permission/source check mới tạo và hiển thị câu trả lời.

Không mặc định phải fine-tune model. RFP không bắt buộc fine-tuning hoặc một model/vendor cụ thể. Không tự huấn luyện từ tài liệu/câu hỏi chưa được cấp quyền.

### 7.3 Bố cục giao diện
Mục tiêu UI đã thống nhất ở mức thiết kế:
- Một bên là Chatbot/question workspace.
- Một bên là Policy/Law evidence viewer.
- Citation có thể mở đúng tài liệu/trang/clause và highlight đoạn evidence.
- Hiển thị tên policy, version, status, effective date, governing date, source, page/clause, applicability và referral.
- Không highlight từ khóa đơn thuần nếu không có evidence đúng.
- Luật và chính sách phải được phân biệt; nội dung giải thích không phải quyết định pháp lý hay phê duyệt.

### 7.4 API, database và security
- API phải có request/response contract, validation và error format thống nhất.
- Authorization kiểm tra ở server-side.
- RBAC/permissions phải được áp dụng trước retrieval và trước display.
- Critical fields dùng kiểu dữ liệu/validation xác định.
- Migration phải có rollback/backup strategy phù hợp.
- Secrets chỉ lưu trong secret manager/environment phù hợp, không commit.
- Logs tối thiểu hóa dữ liệu; không log prompt/source restricted nếu chưa được duyệt.

## 8. Quy tắc riêng cho RAG và policy

Đây là vùng rủi ro cao của dự án; mọi thay đổi phải được kiểm tra cẩn thận.

### 8.1 Retrieval
- Lọc permission, publication state, effective date và scope trước khi đưa evidence ra ngoài.
- Không để vector similarity vượt quyền truy cập hoặc tính áp dụng.
- Giữ nguyên Unicode tiếng Việt, dấu, mã, tên riêng, số tiền, ngày tháng, đơn vị và phủ định.
- Hỗ trợ cách viết tắt/thiếu dấu bằng cơ chế đã test, nhưng không làm sai tên/code/amount/date.
- Source thiếu footnote/table/diagram hoặc không xác minh được phải hold/quarantine theo quy trình.

### 8.2 Answering
Answer package cần thể hiện:
- Câu hỏi.
- Governing date và scope.
- Guidance.
- Exact clause citations.
- Structured fields.
- Missing facts.
- Referral route.

Không được:
- Tự phê duyệt giao dịch.
- Bịa số liệu, field, citation hoặc exception.
- Dùng policy tương lai/withdrawn làm guidance hiện hành.
- Bỏ qua exception hoặc điều kiện áp dụng.
- Trình bày câu trả lời như kết luận pháp lý/chứng nhận tuân thủ.

### 8.3 Conflict và thiếu dữ kiện
Khi có conflict, thiếu owner, thiếu nguồn, thiếu field hoặc không xác định được governing date:
- Dừng câu trả lời hoàn chỉnh.
- Nêu rõ dữ kiện còn thiếu/nguồn xung đột.
- Chuyển đến Policy Owner/đầu mối được chỉ định.
- Ghi audit event phù hợp.
- Không tự chọn rule “có vẻ mới hơn” nếu chưa xác định authority và hiệu lực.

## 9. Quy tắc giao tiếp và phối hợp

- Giao tiếp tôn trọng, tập trung vào vấn đề và evidence.
- Khi cần hỗ trợ, nêu rõ: Issue, việc đã thử, kết quả, điều cần người khác quyết định.
- Không chờ đến cuối Sprint mới báo trễ.
- Không thay đổi requirement bằng lời nói; cập nhật Jira và xin xác nhận.
- Quyết định kỹ thuật cần lưu trong ADR hoặc tài liệu phù hợp.
- Quyết định policy chỉ Policy Owner có thẩm quyền xác nhận.
- Review code là review sản phẩm, không phải đánh giá cá nhân.
- Nếu bất đồng, ghi lại các phương án, trade-off và người có quyền quyết định.

## 10. Change control

Mọi thay đổi scope/requirement phải ghi:
- Requirement/Issue ID và lý do.
- Business Owner/người phê duyệt.
- Tác động cost, timeline, architecture, privacy/rights.
- Gate và test bị ảnh hưởng.
- Quyết định approve/defer/reject.
- Tài liệu/version/ngày hiệu lực.

Không tự ý hấp thụ CRM integration, mailbox histories, OCR, live connectors, automated execution hoặc option O1 vào base scope.

## 11. Quy trình xử lý blocker và incident

### Blocker
1. Cập nhật Jira thành Blocked.
2. Mô tả nguyên nhân, impact, dependency và evidence.
3. Gắn người có thể hỗ trợ.
4. Báo PM/Tech Lead; vấn đề policy báo Policy Owner; privacy/security báo đúng owner.
5. Cập nhật lại khi có thay đổi.

### Incident nghiêm trọng
Áp dụng khi có nguy cơ unauthorized disclosure, false approval, fabricated critical field, sai policy withdrawn/future hoặc credential leak:
- Dừng luồng/chức năng có rủi ro nếu có thể thực hiện an toàn.
- Báo PM, Tech Lead và Security/Privacy/Policy Owner phù hợp ngay.
- Bảo toàn log/evidence hợp pháp; không phát tán thêm dữ liệu.
- Tạo Jira incident/bug P0.
- Không tự xóa evidence hoặc che giấu lỗi.
- Chỉ khôi phục sau khi người có thẩm quyền chấp thuận và có test xác nhận.

## 12. Definition of Ready và Definition of Done

### Definition of Ready
- [ ] Scope và mục tiêu rõ.
- [ ] Acceptance Criteria kiểm chứng được.
- [ ] Priority, Gate, owner, dependency rõ.
- [ ] Source/data có quyền sử dụng.
- [ ] Có test approach và evidence cần nộp.
- [ ] Các quyết định blocking đã được xử lý.

### Definition of Done
- [ ] AC đạt.
- [ ] Code/đầu ra được review.
- [ ] CI và test liên quan pass.
- [ ] Không còn critical/high defect chưa xử lý hoặc chưa được chấp nhận chính thức.
- [ ] Security/privacy impact được xem xét.
- [ ] Docs/ADR/API/schema/migration cập nhật nếu cần.
- [ ] PR và evidence liên kết Jira.
- [ ] QA/verification hoàn tất theo workflow.
- [ ] Không tự nhận Gate đã pass khi chưa có quyết định nghiệm thu.

## 13. Quy tắc đánh giá và “sẹo”

Nếu nhóm sử dụng cơ chế “sẹo” để ghi nhận việc không tuân thủ, phải áp dụng minh bạch:
- Ghi nhận hành vi và bằng chứng cụ thể, không phán xét con người.
- Phân biệt vi phạm cố ý với lỗi do thiếu hướng dẫn, thiếu quyền, blocker hoặc quy trình chưa rõ.
- Người bị ghi nhận được giải trình và đề nghị review.
- Có người xác nhận và log quyết định.
- Không tự động phạt qua Jira/GitHub hoặc dùng điểm trừ để che giấu vấn đề chất lượng.

RFP không quy định chế tài “1 sẹo = -2%, 5 sẹo = -20%”. Nếu nhóm muốn áp dụng công thức này, cần văn bản riêng được toàn nhóm và người quản lý dự án chấp thuận trước khi thực hiện. Không suy ra đây là điều khoản của RFP.

## 14. Checklist “Tôi đã sẵn sàng code chưa?”

- [ ] Tôi đã đọc Team Playbook và các tài liệu liên quan.
- [ ] Tôi hiểu mục tiêu, scope và out of scope của Issue.
- [ ] Issue đạt Definition of Ready.
- [ ] Tôi biết ai là Assignee, reviewer và người quyết định nghiệp vụ.
- [ ] Tôi biết nguồn dữ liệu nào được phép sử dụng.
- [ ] Tôi hiểu ảnh hưởng tới permission, version, effective date, citation và audit (nếu liên quan).
- [ ] Tôi đã tạo branch đúng quy tắc.
- [ ] Tôi biết test nào phải viết/chạy.
- [ ] Tôi biết evidence cần đưa vào PR/Jira.
- [ ] Tôi sẽ cập nhật blocker và tiến độ đúng lúc.

**Nếu bất kỳ mục quan trọng nào chưa rõ: dừng, hỏi và ghi nhận trong Jira trước khi code.**
