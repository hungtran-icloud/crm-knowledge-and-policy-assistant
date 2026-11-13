# 04. Team & Responsibilities – Tổ chức nhân sự

> **Phiên bản:** 0.1 – Role proposal  
> Tên thành viên cụ thể, tỷ lệ phân bổ và quyền phê duyệt phải được PM/Sponsor xác nhận. Một người có thể kiêm nhiều vai trò nhưng không được làm mất tính độc lập của reviewer.

## 1. Team Structure

| Role | Trách nhiệm chính | Deliverables/Accountability |
|---|---|---|
| Project Manager (PM) | Kế hoạch, scope, tiến độ, nguồn lực, risk, change control, status và gate coordination | Project plan, RAID log, meeting notes, gate readiness |
| Business Analyst (BA) | Discovery, stakeholder interview, process mapping, requirement, user story, acceptance criteria | Requirement baseline, process/use cases, traceability |
| Tech Lead / Architect | Kiến trúc, technical decisions, integration boundaries, quality standards, technical risk | Architecture, ADRs, technical review |
| Backend Developer | API, business logic, import, policy lifecycle, auth integration, audit | Backend services, API tests, code |
| AI/RAG Engineer | Data preparation, indexing, retrieval, reranking, grounded answer orchestration, evaluation | RAG pipeline, retrieval metrics, prompt/config tests |
| Frontend Developer | Chat workspace, evidence panel, policy highlight, referral UI, accessibility | UI components, frontend tests |
| Database/Data Engineer | Schema, migrations, import reconciliation, indexes, backup/restore data design | ERD, migrations, data quality reports |
| QA / Test Engineer | Test strategy, test cases, test automation, challenge set, defect triage, independent scoring coordination | Test plan, test evidence, release recommendation |
| DevOps / Platform Engineer | CI/CD, environments, containers, monitoring, backup, recovery, deployment | Pipeline, deployment/restore guide, monitoring |
| Policy Owner (Business) | Approve policy authority, content, exceptions, scope, dates, critical fields and referrals | Signed/recorded policy decisions |
| Knowledge/Data Steward | Prepare permitted exports, curated text, source references, metadata, version, permission and withdrawal | Approved import package and reconciliation |
| Privacy/Security/Legal Owner | Review processing, access, provider, retention, incidents, AI classification and legal applicability | Dated governance review and approvals |
| Staff User / Pilot Participant | Supply real questions, inspect evidence, record correction and effort | Pilot feedback and usage evidence |
| Sponsor / Purchaser | Scope, funding, gate decisions, route selection and escalation | G0–G4 decisions |

## 2. RACI Matrix

Legend: `R` Responsible, `A` Accountable, `C` Consulted, `I` Informed. Một hoạt động chỉ nên có một A cuối cùng.

| Activity | Sponsor | PM | BA | Tech Lead | Dev Team | QA | Policy Owner | Steward | Privacy/Sec |
|---|---|---|---|---|---|---|---|---|---|
| Approve scope/budget | A | R | C | C | I | I | C | I | C |
| Requirement baseline | I | A | R | C | C | C | C | C | C |
| Policy authority/date | I | C | C | I | I | C | A/R | R | C |
| Source preparation/import | I | A | C | C | R | C | C | R | C |
| Architecture/ADR | I | C | C | A/R | R | C | I | C | C |
| Implementation | I | A | C | R | R | C | C | C | C |
| Test strategy/evaluation | I | C | C | C | C | A/R | C | C | C |
| Independent policy scoring | I | C | C | I | I | R | A/R* | C | I |
| Privacy/security review | I | C | I | C | C | C | C | C | A/R |
| G0/Gate decision | A | R | C | C | I | C | C | C | C |
| Pilot operation | I | A | C | C | R | R | R | C | C |
| Handover | I | A | C | R | R | C | C | C | C |

`*` Reviewer nghiệp vụ độc lập cần được chỉ định. Người phát triển/tune hệ thống không được tự làm independent reviewer cho sealed acceptance cases.

## 3. Role Boundaries

- **PM** quản lý tiến độ, không tự quyết định nội dung policy.
- **BA** làm rõ yêu cầu, không tự đặt ra quy tắc nghiệp vụ chưa được owner duyệt.
- **Tech Lead** quyết định kỹ thuật trong phạm vi được ủy quyền, không thay thế legal/security owner.
- **Developers** triển khai theo requirement đã duyệt, không tự tạo critical policy values.
- **QA** kiểm tra và báo cáo bằng chứng; không sửa tiêu chí nghiệm thu sau khi biết kết quả.
- **Policy Owner** chịu trách nhiệm authority/content/exception/effective date.
- **Steward** chuẩn bị và quản lý dữ liệu nguồn; không tự phê duyệt nội dung policy nếu không có quyền.
- **Privacy/Security/Legal Owner** xác nhận tính áp dụng và kiểm soát theo vai trò; không mặc định local hosting/encryption đồng nghĩa compliance.

## 4. Team Operating Rules

1. Mỗi Jira Issue có một Assignee chịu trách nhiệm chính.
2. PR cần reviewer khác người tạo PR.
3. Critical acceptance cases do reviewer độc lập chấm.
4. Blocker phải có nguyên nhân, owner hỗ trợ và next action.
5. Quyết định policy phải được ghi lại cùng owner và thời điểm.
6. Quyết định kiến trúc quan trọng phải có ADR.
7. Không chia sẻ dữ liệu thật qua kênh không được phê duyệt.

## 5. Meeting Cadence

| Meeting | Tần suất | Thời lượng | Thành phần | Kết quả |
|---|---|---:|---|---|
| Team sync / stand-up | Mỗi 2 ngày | 15–20 phút | Team | Update Jira, blockers, next actions |
| Sprint Planning | Đầu Sprint | 45–90 phút | PM, team, BA, QA | Sprint Goal, committed issues |
| Backlog Refinement | 1 lần/Sprint hoặc khi cần | 30–60 phút | BA, Tech Lead, team | Ready backlog |
| Sprint Review | Cuối Sprint | 30–60 phút | Team, stakeholders | Demo/evidence, feedback |
| Retrospective | Cuối Sprint | 30 phút | Team | Improvement actions |
| Gate Review | Trước G0–G4 | Theo agenda | Sponsor, owners, PM, QA | Gate decision |

### 5 câu hỏi trong team sync

1. What did you do?
2. What are you doing?
3. What will you do next?
4. Do you need help?
5. Any other questions?

Báo cáo theo Jira Issue Key. Các thảo luận kỹ thuật sâu chuyển sang meeting riêng.

## 6. Open Items

- Điền tên thành viên và role thực tế.
- Chỉ định Policy Owner và substitute cho từng family.
- Chỉ định independent reviewers.
- Xác nhận người có quyền approve G0–G4.
- Xác nhận meeting calendar và timezone Asia/Ho_Chi_Minh.
