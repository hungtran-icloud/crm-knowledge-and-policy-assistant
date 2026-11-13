# Quy tắc sử dụng Jira
> **Dự án:** SongNhat CRM Knowledge & Policy Assistant  
> **Loại tài liệu:** Quy trình làm việc bắt buộc của nhóm  
> **Phiên bản:** 1.0 – Working Agreement  
> **Trạng thái:** Đề xuất áp dụng nội bộ; Project Manager/Tech Lead xác nhận trước Sprint kế tiếp.

## 1. Mục đích và nguyên tắc

Jira là **nguồn sự thật về công việc và tiến độ**. GitHub là nguồn sự thật về mã nguồn, Pull Request và lịch sử thay đổi. Không dùng tin nhắn chat thay cho Jira để giao việc hoặc xác nhận hoàn thành.

Nguyên tắc:
1. Không có Jira Issue thì chưa được xem là công việc đã được giao chính thức.
2. Mỗi Issue có một người chịu trách nhiệm chính (Assignee).
3. Công việc phải có mô tả, mục tiêu, Acceptance Criteria và mức ưu tiên trước khi đưa vào Sprint.
4. Cập nhật Jira ngay khi trạng thái, phạm vi, người phụ trách hoặc kế hoạch thay đổi.
5. Không tự ý đổi phạm vi, Release Gate hoặc tiêu chí nghiệm thu.
6. Không đánh dấu Done chỉ vì đã viết code; phải có bằng chứng kiểm thử/review và đáp ứng Definition of Done.
7. Jira không phải nơi lưu secrets, token, dữ liệu khách hàng hoặc tài liệu chính sách bị hạn chế quyền.

## 2. Cấu trúc quản lý công việc

### 2.1 Issue types

| Loại | Dùng khi nào | Ví dụ |
|---|---|---|
| Epic | Nhóm năng lực lớn hoặc workstream | Knowledge Base & Data Import |
| Story | Nhu cầu/nghiệp vụ có giá trị cho người dùng | Nhân viên tra cứu điều khoản đang có hiệu lực |
| Task | Công việc kỹ thuật/nghiệp vụ có đầu ra cụ thể | Xây dựng bộ kiểm tra CSV import |
| Bug | Hành vi sai so với yêu cầu/AC | Kết quả lấy nhầm policy đã withdrawn |
| Spike | Nghiên cứu có timebox và kết luận cần bàn giao | So sánh API model và local model |
| Sub-task | Phần việc nhỏ của một Issue cha | Viết unit test cho date resolver |

Không tạo Epic cho từng thành viên hoặc từng Sprint. Không dùng Task để che giấu một Story có giá trị người dùng rõ ràng.

### 2.2 Epic baseline

Dùng các Epic nền sau, trừ khi PM/BA điều chỉnh có ghi nhận:

- EP01 – Discovery & Requirement Analysis
- EP02 – Knowledge Base & Data Import
- EP03 – Policy Management & Version Control
- EP04 – AI Retrieval & Question Answering
- EP05 – User Interface & Evidence Viewer
- EP06 – Security, Privacy & Governance
- EP07 – Testing, Evaluation & Acceptance
- EP08 – Deployment, Monitoring & Handover

### 2.3 Liên kết với Release Gates

RFP xác định năm Release Gates **G0–G4**. Gate là điều kiện ra quyết định/nghiệm thu, không mặc định đồng nghĩa với một Sprint.

| Gate | Ý nghĩa | Jira cần theo dõi |
|---|---|---|
| G0 | Ready to build | Phạm vi, policy families, nguồn được phép, owners, quyền, capacity, route comparison |
| G1 | Controlled offline | Corpus/field rows được duyệt, import reconciliation, permissions, dates, conflicts, references |
| G2 | Supervised use | Quality/challenge tests, không có critical defect, legal deployment review, training và fallback |
| G3 | Pilot acceptance | Kết quả supervised use tối thiểu 20 ngày làm việc; báo cáo effort/use/cost |
| G4 | Handover | Code, cấu hình, tài liệu, training, restore/exit evidence |

Mỗi Issue thuộc phạm vi triển khai phải gắn Release Gate phù hợp. Không tự ghi “Gate passed”; chỉ người được giao quyền nghiệm thu mới cập nhật quyết định Gate và đính kèm evidence.

## 3. Quy tắc tạo Issue

Mỗi Story/Task/Bug phải có các trường sau:

- **Summary:** ngắn gọn, bắt đầu bằng động từ hoặc mô tả lỗi.
- **Context/Description:** vấn đề, lý do, phạm vi và kết quả cần đạt.
- **Acceptance Criteria:** tiêu chí kiểm chứng được, ưu tiên Given/When/Then.
- **Priority:** P0/P1/P2/P3 theo mục 6.
- **Epic Link/Parent:** Epic hoặc Issue cha liên quan.
- **Release Gate:** G0/G1/G2/G3/G4 hoặc “N/A” có lý do.
- **Component/Workstream:** ví dụ Backend, Frontend, RAG, Policy, QA, DevOps.
- **Assignee:** một người chịu trách nhiệm chính.
- **Sprint:** chỉ gán khi Issue đã sẵn sàng và được chọn vào Sprint.
- **Estimate:** dùng đơn vị nhóm thống nhất; không tự quy đổi giữa story point và giờ.
- **Dependencies/Blocked by:** liên kết Issue phụ thuộc.
- **Evidence/Links:** tài liệu, PR, test report hoặc quyết định có liên quan.

### Mẫu mô tả Story/Task

```markdown
## Context
Vấn đề hoặc nhu cầu cần giải quyết.

## Scope
- In scope:
- Out of scope:

## Acceptance Criteria
- [ ] Given ... When ... Then ...
- [ ] ...

## Dependencies
- ...

## Test / Evidence
- ...

## Release Gate
Gx
```

### Mẫu Bug

```markdown
## Environment
## Steps to reproduce
1.
2.

## Expected result
## Actual result
## Severity / Impact
## Evidence (đã loại bỏ dữ liệu nhạy cảm)
## Acceptance criteria for fix
```

Không tạo Issue trùng lặp; tìm kiếm trước khi tạo. Nếu phát hiện trùng, liên kết và đóng Issue trùng với lý do.

## 4. Workflow và cập nhật trạng thái

Workflow đề xuất:

`Backlog → Selected for Development → In Progress → In Review → QA / Verification → Done`

Các trạng thái phụ:
- **Blocked:** đang bị chặn bởi dependency, quyền truy cập, quyết định hoặc lỗi ngoài khả năng xử lý ngay.
- **Rejected / Won't Do:** không thực hiện; phải có lý do và người quyết định.
- **Reopened:** chỉ dùng khi tiêu chí chưa đạt hoặc lỗi tái xuất hiện.

Quy tắc:
- Chỉ chuyển sang **In Progress** khi người thực hiện đã nhận việc và bắt đầu.
- Chuyển **In Review** khi code/đầu ra đã sẵn sàng review và có link PR/evidence.
- Chuyển **QA / Verification** sau khi review/merge theo workflow nhóm và cần kiểm thử xác nhận.
- Chuyển **Done** khi tất cả Acceptance Criteria và DoD đạt.
- Chuyển **Blocked** ngay khi không thể tiếp tục; ghi rõ blocker, người cần hỗ trợ và thời điểm cập nhật tiếp theo.
- Không để Issue ở In Progress mà không có cập nhật quá 2 ngày làm việc. Nếu chưa có tiến triển, nêu lý do hoặc đề nghị hỗ trợ.
- Không dùng trạng thái để thể hiện cảm xúc hoặc gây áp lực cá nhân.

Nếu Jira workflow thực tế khác, PM cấu hình một workflow thống nhất và cập nhật tài liệu này; không tự tạo status riêng.

## 5. Sprint rules

### Trước Sprint Planning
- Product/Business Owner và BA làm rõ yêu cầu, scope và Acceptance Criteria.
- Tech Lead làm rõ phụ thuộc, rủi ro kỹ thuật và các quyết định cần ADR.
- QA xác định test approach và dữ liệu kiểm thử được phép.
- Thành viên cập nhật availability và việc còn dang dở.

### Trong Sprint Planning
- Chốt **Sprint Goal** trước khi chọn Issue.
- Chỉ chọn Issue đủ rõ, có owner, AC và estimate.
- Ưu tiên theo Release Gate, rủi ro và dependency; không chỉ chọn việc dễ.
- Không cam kết vượt capacity thực tế.
- Ghi lại Sprint Goal, danh sách Issue, estimate và dependency.

### Trong Sprint
- Không tự ý thêm scope. Việc khẩn cấp phải được PM/PO và Tech Lead đánh giá tác động; nếu thêm việc thì thống nhất việc nào bị bỏ/đẩy.
- Chia Issue lớn thành các phần có thể review và kiểm thử.
- Cập nhật Jira trước buổi sync, không đợi PM hỏi.
- Blocker có owner xử lý và ETA; nếu chưa có ETA thì ghi “chưa xác định”.

### Sprint Review / Retrospective
- Demo theo Acceptance Criteria và evidence.
- Issue chưa Done phải quay về Backlog/Sprint sau theo quyết định của nhóm; không giữ Done giả.
- Ghi action items của retrospective thành Jira Issue nếu cần theo dõi.

## 6. Priority và severity

| Mức | Ý nghĩa | Ví dụ |
|---|---|---|
| P0 – Critical | Rủi ro an toàn, quyền, privacy, false approval, sai policy có thể gây hậu quả nghiêm trọng | Lộ dữ liệu trái quyền; dùng policy withdrawn như hiện hành |
| P1 – High | Chức năng cốt lõi hoặc điều kiện bắt buộc của Gate hiện tại | Citation sai; date/scope resolver sai |
| P2 – Medium | Cải thiện usability/operation, chưa block Gate | Bộ lọc hoặc thông báo chưa tối ưu |
| P3 – Low | Nice-to-have hoặc option chưa được duyệt | Tùy biến giao diện không thiết yếu |

Bug severity phản ánh mức ảnh hưởng; Priority phản ánh thứ tự xử lý. Không tự hạ mức P0/P1 để làm đẹp báo cáo. Việc đổi mức phải có lý do và người quyết định.

## 7. Quy tắc Blocked và Escalation

Khi bị Blocked, cập nhật:
1. Điều gì đang chặn?
2. Tác động tới Issue/Gate/Sprint nào?
3. Ai có thể gỡ blocker?
4. Đã thử cách nào?
5. Khi nào cập nhật lại?

Escalate ngay với PM/Tech Lead nếu blocker liên quan đến:
- Policy Owner/authority chưa rõ.
- Quyền sử dụng nguồn, dữ liệu cá nhân hoặc provider chưa được duyệt.
- Source thiếu trang, footnote, bảng hoặc bản gốc.
- Policy version/effective date/conflict chưa giải quyết.
- Rủi ro P0 hoặc nguy cơ làm sai điều kiện nghiệm thu.

## 8. Liên kết Jira ↔ GitHub

- Branch, commit và PR phải chứa Jira Issue Key, ví dụ `SON-123`.
- PR phải liên kết Jira Issue tương ứng.
- Jira Issue cập nhật link PR, trạng thái review, test evidence và kết quả.
- Merge PR không tự động có nghĩa Jira Issue Done.
- Jira Done phải phản ánh đầu ra đã đáp ứng AC/DoD.
- Không dùng một Jira Issue để gom nhiều thay đổi không liên quan chỉ nhằm giảm số lượng ticket.

## 9. Daily sync hai ngày một lần

Nhóm sync mỗi 2 ngày, thời lượng đề xuất 15–20 phút. Trước buổi họp, mỗi thành viên tự cập nhật Jira và trả lời:

1. What did you do? – Bạn đã hoàn thành gì kể từ lần sync trước?
2. What are you doing? – Bạn đang làm Issue nào?
3. What will you do next? – Bước tiếp theo là gì?
4. Do you need help? – Có blocker/cần hỗ trợ không?
5. Any other questions? – Có câu hỏi hoặc quyết định cần làm rõ không?

Báo cáo theo Jira Issue Key. Không biến daily sync thành buổi debug dài; tách cuộc họp kỹ thuật riêng cho người liên quan.

## 10. Quy tắc chất lượng và dữ liệu

- Không đưa dữ liệu khách hàng thật, thông tin cá nhân, credential hoặc policy restricted vào mô tả Jira nếu không được phép.
- Dùng dữ liệu giả lập/đã được phép cho screenshot và test evidence.
- Sealed acceptance cases phải được kiểm soát quyền truy cập; developer không được tune trên sealed cases.
- Mọi thay đổi ảnh hưởng policy, quyền, effective date, source state hoặc critical fields phải có test/evidence tương ứng.
- Không ghi nội dung AI trả lời là “đúng” nếu chưa đối chiếu nguồn, phiên bản và clause áp dụng.

## 11. Definition of Ready (DoR)

Issue sẵn sàng vào Sprint khi:
- [ ] Mục tiêu và phạm vi rõ.
- [ ] Acceptance Criteria kiểm chứng được.
- [ ] Priority và Release Gate đã xác định.
- [ ] Owner và dependency đã rõ.
- [ ] Có đủ tài liệu/nguồn được phép để thực hiện.
- [ ] Có cách kiểm thử hoặc xác minh.
- [ ] Không có câu hỏi blocking chưa có người xử lý.

## 12. Definition of Done (DoD)

Issue chỉ Done khi:
- [ ] Acceptance Criteria đạt.
- [ ] Code/đầu ra đã được review.
- [ ] Test liên quan pass và có evidence.
- [ ] Không còn defect Critical/High chưa xử lý hoặc chưa được chấp nhận chính thức.
- [ ] Security/privacy impact đã được xem xét.
- [ ] Docs/ADR/migration được cập nhật nếu cần.
- [ ] PR và evidence đã liên kết trong Jira.
- [ ] Assignee cập nhật kết quả cuối cùng và ghi chú vận hành nếu cần.

## 13. Quy tắc ghi nhận vi phạm và “sẹo”

Nếu nhóm áp dụng cơ chế “sẹo” nội bộ (ví dụ mức trừ điểm đã được nhóm thống nhất), việc ghi nhận phải:
- Dựa trên hành vi/quy trình cụ thể và bằng chứng Jira/GitHub, không dựa trên cảm tính.
- Phân biệt lỗi vô ý, thiếu năng lực, thiếu nguồn lực và cố tình bỏ qua quy trình.
- Có người ghi nhận, ngày, Issue liên quan, mô tả, mức ảnh hưởng và cơ hội giải trình.
- Có quyền yêu cầu xem xét lại.
- Không tự động biến điểm trừ thành đánh giá nhân sự hoặc tiền phạt.
- Không áp dụng hồi tố và không tự ý thay đổi công thức.

**Chưa có căn cứ trong RFP để xác lập mức phạt “1 sẹo = -2%, 5 sẹo = -20%”.** Nếu nhóm muốn áp dụng, cần chốt bằng văn bản riêng: đối tượng bị tính, đơn vị tính, kỳ đánh giá, trường hợp miễn trừ, cách khiếu nại và người phê duyệt. Không cấu hình automation phạt điểm trước khi có xác nhận đó.

## 14. Checklist thành viên

- [ ] Tôi kiểm tra Jira trước khi bắt đầu việc.
- [ ] Tôi chỉ nhận Issue có scope/AC rõ.
- [ ] Tôi cập nhật trạng thái và blocker kịp thời.
- [ ] Tôi liên kết branch/commit/PR với Jira Key.
- [ ] Tôi không tự đánh dấu Done khi chưa đủ evidence.
- [ ] Tôi không đưa dữ liệu/secret không được phép vào Jira.
