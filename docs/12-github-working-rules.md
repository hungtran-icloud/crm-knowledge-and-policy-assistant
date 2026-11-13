# Quy tắc sử dụng GitHub
> **Dự án:** SongNhat CRM Knowledge & Policy Assistant  
> **Loại tài liệu:** Quy trình làm việc bắt buộc của nhóm  
> **Phiên bản:** 1.0 – Working Agreement  
> **Trạng thái:** Đề xuất áp dụng nội bộ; Tech Lead xác nhận branch protection và CI trước khi merge code đầu tiên.

## 1. Mục đích và nguyên tắc

GitHub là **nguồn sự thật của mã nguồn, lịch sử thay đổi, Pull Request và kiểm tra tự động**.

- Không push trực tiếp lên `main`.
- Mọi thay đổi phải có Jira Issue Key hoặc lý do ngoại lệ được Tech Lead chấp thuận.
- Mọi thay đổi code phải đi qua Pull Request (PR), review và CI.
- Không commit secrets, dữ liệu khách hàng, policy restricted hoặc dữ liệu không có quyền sử dụng.
- Không merge khi CI bắt buộc fail hoặc còn review comment blocking.
- Không dùng GitHub Issues thay Jira để quản lý Sprint/Backlog nếu nhóm đã thống nhất Jira là công cụ quản lý công việc.

## 2. Repository baseline

Tên repository đề xuất: `songnhat-crm-knowledge-policy-assistant`.

Quyền truy cập:
- Cấp quyền theo nguyên tắc least privilege.
- Bật MFA cho tài khoản có quyền ghi/maintain/admin.
- Chỉ cấp quyền Admin cho người thực sự cần quản trị repository.
- Thành viên rời nhóm phải được thu hồi quyền kịp thời.
- Không chia sẻ tài khoản hoặc personal access token.

Các thiết lập bảo vệ đề xuất:
- Protect `main`; require PR.
- Require ít nhất 1 approval từ người khác tác giả.
- Require CI status checks pass.
- Dismiss stale approvals khi có commit mới làm thay đổi nội dung review.
- Require conversation resolution.
- Block force push và branch deletion trên branch bảo vệ.
- Bật secret/dependency scanning nếu gói GitHub và cấu hình cho phép.
- Không giả định tính năng nào đã bật; Repository Admin phải kiểm tra thực tế.

## 3. Branch strategy

### 3.1 Branch chính

| Branch | Mục đích |
|---|---|
| `main` | Nhánh ổn định, chỉ nhận thay đổi đã review và pass CI |
| `develop` | Nhánh tích hợp nếu nhóm chọn GitFlow; chỉ dùng khi đã cấu hình và thống nhất |

Khuyến nghị ban đầu: dùng `main` làm nhánh tích hợp nếu dự án chưa cần release flow phức tạp. Chỉ tạo `develop` khi Tech Lead ghi rõ lý do và cách release trong ADR. Không duy trì hai mô hình song song một cách tùy tiện.

### 3.2 Branch làm việc

Format:

```text
<type>/SON-<issue-number>-<short-description>
```

Types:
- `feature/` – chức năng mới.
- `fix/` – sửa lỗi.
- `hotfix/` – sửa lỗi khẩn cấp trên bản release.
- `docs/` – tài liệu.
- `test/` – bổ sung/sửa test.
- `refactor/` – tái cấu trúc không đổi hành vi.
- `chore/` – tooling, dependency, cấu hình.

Ví dụ:

```text
feature/SON-123-policy-search
fix/SON-145-withdrawn-policy-filter
docs/SON-151-local-development-guide
test/SON-162-effective-date-cases
```

Quy tắc:
- Tạo branch từ base branch mới nhất.
- Một branch tập trung một Issue hoặc một mục tiêu liên quan chặt chẽ.
- Không đặt tên `test`, `final`, `new-code`, `my-branch`.
- Không dùng branch của người khác nếu chưa thống nhất.
- Xóa branch sau khi merge nếu không còn cần thiết.

## 4. Commit convention

Format:

```text
<type>(<scope>): <imperative description> [SON-123]
```

Types:
- `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `security`, `build`, `ci`.

Ví dụ:

```text
feat(retrieval): add policy passage search [SON-123]
fix(policy): exclude withdrawn policy version [SON-145]
test(policy): cover future effective date [SON-162]
docs(api): describe question endpoint [SON-151]
security(auth): enforce policy source permission [SON-170]
```

Quy tắc:
- Mô tả ngắn, rõ, dùng tiếng Anh nhất quán trong commit message.
- Một commit nên đại diện một thay đổi logic có thể hiểu/review.
- Không commit message mơ hồ như `update`, `fix`, `done`, `final`.
- Không commit file sinh tự động, cache, môi trường local hoặc file secrets.
- Không rewrite shared branch hoặc force push nếu chưa có sự đồng ý của người liên quan.

## 5. Pull Request (PR)

### 5.1 Trước khi mở PR

- [ ] Jira Issue đã tồn tại và có Acceptance Criteria.
- [ ] Branch đúng naming convention.
- [ ] Code đã format/lint và test local.
- [ ] Không chứa secrets, dữ liệu thật hoặc file không cần thiết.
- [ ] Đã cập nhật docs/API/ADR/migration khi cần.
- [ ] Đã rebase/merge base branch theo quy trình nhóm, xử lý conflict cẩn thận.

### 5.2 PR title

Format:

```text
[SON-123] feat: add policy evidence viewer
```

### 5.3 PR description template

```markdown
## Jira
- Issue: SON-123
- Link:

## Why
Vấn đề hoặc mục tiêu của thay đổi.

## What changed
- ...
- ...

## Scope / Out of scope
- In:
- Out:

## How to test
1.
2.

## Test results
- Unit:
- Integration/API:
- Manual:

## Risk & impact
- Security/privacy:
- Data migration:
- API compatibility:
- Policy/date/permission impact:

## Evidence
- Screenshot/log/test report (đã loại bỏ dữ liệu nhạy cảm):

## Checklist
- [ ] Acceptance Criteria được đáp ứng.
- [ ] Tests đã thêm/cập nhật và pass.
- [ ] Lint/format pass.
- [ ] Docs/ADR/migration cập nhật nếu cần.
- [ ] Không có secrets hoặc dữ liệu không được phép.
- [ ] Không có critical/high defect chưa xử lý.
```

### 5.4 Quy tắc PR

- PR phải nhỏ nhất có thể nhưng vẫn hoàn chỉnh về mặt logic.
- Tác giả không tự approve PR của mình.
- Ít nhất 1 reviewer độc lập.
- Thay đổi liên quan authentication, authorization, privacy, policy authority, effective dates, critical fields hoặc audit cần reviewer phù hợp (Tech Lead/Security/Policy owner tùy nội dung).
- Reviewer phải kiểm tra yêu cầu, logic, test, bảo mật, khả năng vận hành và tác động dữ liệu.
- Tác giả phản hồi comment; comment blocking phải được giải quyết trước merge.
- Không merge PR chỉ vì gần deadline.
- PR draft dùng cho trao đổi sớm, không được merge khi chưa hoàn thiện.
- PR thay đổi policy source hoặc nội dung chính sách không tự cấp quyền phê duyệt policy; phải có Policy Owner approval ngoài code review.

## 6. Code review checklist đặc thù dự án

### General
- [ ] Thay đổi đúng Jira scope và AC.
- [ ] Code dễ đọc, có type/validation phù hợp.
- [ ] Không thêm dependency không cần thiết.
- [ ] Error handling không che giấu lỗi.
- [ ] Có test cho happy path và negative path.

### RAG / Knowledge / Policy
- [ ] Permission, publication state, effective date và scope được lọc trước khi đưa evidence vào context.
- [ ] Policy conflict/ambiguous source được hold hoặc referral, không tự chọn theo suy đoán.
- [ ] Citation trỏ đúng nguồn, phiên bản, clause và vị trí.
- [ ] Không biến text do model sinh ra thành critical structured field.
- [ ] Không trả lời hoàn chỉnh trước final source/permission check.
- [ ] Historical answer hiển thị governing date và trạng thái lịch sử phù hợp.
- [ ] Không tự động cập nhật policy hoặc tự huấn luyện từ câu hỏi/feedback.
- [ ] Không có false approval hoặc nội dung vượt thẩm quyền của assistant.

### Security / Privacy
- [ ] Authorization được kiểm tra phía server.
- [ ] Không lộ dữ liệu qua log, cache, snippet, export hoặc error message.
- [ ] Không có secrets/PII trong fixtures, screenshot hoặc test artifacts.
- [ ] Thay đổi có audit event phù hợp nếu liên quan.

## 7. Merge rules

Chỉ merge khi:
- PR liên kết đúng Jira Issue.
- Approval bắt buộc đã có.
- CI required checks pass.
- Không còn unresolved blocking comments.
- Test evidence và docs đã cập nhật.
- Reviewer xác nhận scope và rủi ro.
- Với thay đổi có ảnh hưởng Gate, evidence cần thiết được đính kèm.

Ưu tiên Squash and Merge nếu nhóm muốn lịch sử `main` gọn; chọn merge strategy một lần và ghi trong repository settings. Không thay đổi chiến lược theo cảm tính từng PR.

Sau merge:
1. Kiểm tra merge commit/PR.
2. Cập nhật Jira Issue với PR và evidence.
3. Chuyển Jira sang trạng thái phù hợp; không tự đánh dấu Done nếu chưa QA/verification.
4. Xóa branch nếu không cần.
5. Theo dõi CI/deployment nếu PR có kích hoạt pipeline.

## 8. Releases và tags

- Chỉ tạo release/tag theo quy ước version được Tech Lead thống nhất.
- Release note phải nêu thay đổi, migration, known issues và rollback note.
- Không gắn tag release cho build chưa qua test/release gate tương ứng.
- GitHub Release không thay thế quyết định G1–G4; Gate acceptance cần evidence và người có thẩm quyền.

## 9. CI và kiểm tra tự động

Pipeline tối thiểu đề xuất:
- Formatting/lint.
- Type/static checks phù hợp stack.
- Unit tests.
- Integration/API tests khi môi trường cho phép.
- Dependency/security checks nếu khả dụng.
- Build/package check.

Quy tắc:
- Required checks phải được Repository Admin cấu hình thực tế.
- Không bỏ qua CI bằng cách xóa test hoặc disable workflow để merge.
- Flaky test phải tạo Issue, có owner và kế hoạch sửa; không được che giấu.
- Không đưa secret vào workflow YAML; dùng GitHub Secrets/Environment secrets và quyền tối thiểu.
- CI không được truy cập sealed acceptance set nếu không có phê duyệt.

## 10. Quản lý dữ liệu và tài liệu

Không commit:
- `.env`, token, password, private key.
- Customer records/dossiers hoặc dữ liệu cá nhân thật trong base scope.
- Source policy chưa được cấp quyền hoặc bản sao không được phép.
- Sealed acceptance cases hoặc đáp án chuẩn nếu người phát triển không được quyền truy cập.
- Database dump, log thật, file cache, model weights lớn chưa được phê duyệt.

Nên commit:
- `.env.example` chỉ chứa placeholder.
- Synthetic fixtures hoặc test data được phê duyệt.
- Schema, migration, source mapping và tài liệu có quyền phân phối.
- ADR, test plan, runbook và hướng dẫn setup.

RFP xác định base scope không nhập customer records. Option O1 là phạm vi riêng, chỉ được xem xét khi identity, permissions, lawful processing và incremental value được xác minh. Không đưa tích hợp O1 vào code mặc định nếu chưa có quyết định scope.

## 11. Xử lý sự cố

- Nếu lộ secret: thu hồi/rotate ngay, báo Repository Admin và Security Owner; xóa khỏi lịch sử không thay thế việc rotate.
- Nếu phát hiện lộ dữ liệu: dừng chia sẻ/deploy liên quan, bảo toàn evidence cần thiết và báo đúng đầu mối.
- Nếu merge nhầm: tạo incident/bug, xác định impact, rollback hoặc hotfix qua PR; không sửa trực tiếp trên `main`.
- Nếu CI/deploy lỗi: ghi nhận run URL, commit SHA, môi trường, thời điểm và owner xử lý.

## 12. Checklist thành viên

- [ ] Tôi tạo branch từ base mới nhất và có Jira Key.
- [ ] Commit message theo convention.
- [ ] Tôi không push trực tiếp lên branch bảo vệ.
- [ ] PR có mục tiêu, test plan, evidence và risk impact.
- [ ] Tôi review cả logic, test, permission/date/citation khi liên quan.
- [ ] Tôi không approve PR của chính mình.
- [ ] Tôi không merge khi CI fail hoặc còn comment blocking.
- [ ] Tôi cập nhật Jira sau merge.
