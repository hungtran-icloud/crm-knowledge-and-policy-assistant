# 07. Project Management Tools – Công cụ quản lý

> **Phiên bản:** 0.1 – Tooling proposal  
> Công cụ chỉ được xem là đã kết nối/cấu hình sau khi Admin xác nhận thực tế.

## 1. Tool Matrix

| Công cụ | Mục đích | Quy tắc sử dụng |
|---|---|---|
| Jira | Backlog, Epic, Story, Task, Bug, Sprint, status, priority, estimate, blocker | Nguồn chuẩn về công việc/tiến độ |
| GitHub | Repository, source code, branch, commit, PR, Issues nếu được thống nhất, Actions | Nguồn chuẩn về code/review/CI |
| Figma | Wireframe, UI/UX prototype | Lưu link thiết kế vào Jira/Docs |
| Discord/Slack/Teams | Trao đổi nhóm và meeting | Quyết định quan trọng phải ghi lại trong Jira/ADR/docs |
| Google Drive/SharePoint | Tài liệu nghiệp vụ và file được cấp quyền | Quản lý quyền; không upload data nhạy cảm tùy tiện |
| Swagger/OpenAPI | API contract/documentation | Sinh hoặc cập nhật từ API contract được version-control |
| Docker | Local development và packaging | Dùng config reproducible, không chứa secret |
| GitHub Actions | CI/CD | Test/lint/build/security checks |
| PostgreSQL/pgvector | Persistence/search (đề xuất) | Chỉ chốt sau ADR/PoC |
| Monitoring/logging platform | Quan sát hệ thống | Theo privacy/retention policy |

## 2. Jira Configuration

### Issue hierarchy

- Epic: nhóm workstream.
- Story: yêu cầu có giá trị người dùng.
- Task: công việc kỹ thuật/phi chức năng.
- Bug: lỗi.
- Sub-task: phần việc nhỏ.

### Epics đề xuất

1. EP01 Discovery & Requirement Analysis.
2. EP02 Knowledge Base & Data Import.
3. EP03 Policy Management & Version Control.
4. EP04 AI Retrieval & Question Answering.
5. EP05 User Interface & Referral.
6. EP06 Security, Privacy & Governance.
7. EP07 Testing, Evaluation & Acceptance.
8. EP08 Deployment, Monitoring & Handover.

### Workflow đề xuất

`To Do → In Progress → In Review → Done`

`Blocked` là trạng thái riêng hoặc flag tùy cấu hình Jira. Mỗi blocker phải có reason, owner/support needed và next action.

### Required fields

- Summary, Description.
- Acceptance Criteria.
- Assignee.
- Priority.
- Epic Link/Parent.
- Sprint.
- Release Gate: G0/G1/G2/G3/G4.
- Workstream.
- Estimate.
- Dependencies.
- PR/Evidence URL.

## 3. GitHub Configuration

- Repository private theo policy dự án.
- Protected branches.
- PR template.
- Issue/bug templates nếu dùng GitHub Issues.
- CODEOWNERS cho module nhạy cảm.
- Actions workflows cho lint/test/build.
- `.gitignore`, `.env.example`, README.
- Dependency/secret scanning nếu khả dụng.
- Release tags và changelog.

## 4. Jira–GitHub Traceability

| Event | Required action |
|---|---|
| Task ready | Jira Issue có AC và Assignee |
| Start work | Branch chứa Jira Key |
| Commit | Commit message chứa Jira Key |
| PR | PR link về Jira Issue |
| Review | Review decision và comments |
| Merge | Branch protection/CI pass |
| Done | Jira có PR/commit/test evidence |

## 5. Communication Rules

- Jira: task, priority, blocker, deadline, scope decision.
- GitHub: code discussion, PR review, technical implementation.
- ADR/docs: architecture and project decisions.
- Chat: trao đổi nhanh; quyết định phải được ghi lại.
- Figma: thiết kế và comment UI.

## 6. Tool Access & Permissions

- Cấp quyền theo least privilege.
- Không dùng tài khoản chung.
- Bật MFA nếu nền tảng hỗ trợ.
- Offboarding phải thu hồi quyền.
- Secrets không đặt trong Jira description, chat hoặc Git commit.
- Tài liệu chính sách và dữ liệu test chỉ chia sẻ với nhóm được phép.

## 7. Open Items

- Jira project key và workflow thực tế.
- GitHub organization/repository URL.
- Chốt có dùng `develop` hay trunk-based/PR-to-main.
- Chốt công cụ chat và lưu trữ tài liệu.
- Chốt Figma workspace và người quản trị.
- Xác nhận connector/plugin và quyền truy cập; không mặc định đã tích hợp.
