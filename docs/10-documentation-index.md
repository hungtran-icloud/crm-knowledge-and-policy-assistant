# 10. Documentation – Tài liệu dự án

> **Phiên bản:** 0.1 – Documentation index  
> Tài liệu là bộ khung ban đầu; các mục đánh dấu `TBD` cần được cập nhật sau khi có quyết định/kiểm chứng.

## 1. Documentation Register

| Tài liệu | Mục đích | Trạng thái |
|---|---|---|
| README.md | Tổng quan, prerequisites, setup/run/test | Draft |
| Project Overview | Mục tiêu, scope, users, outcomes | Draft |
| SRS / Requirements | Business/functional/non-functional requirements, use cases, AC | Draft |
| Project Plan | Timeline, milestones, sprint, risks, deliverables | Draft |
| Team & Responsibilities | Role, RACI, meeting cadence | Draft |
| Architecture Document | Architecture, components, data flow, deployment | Proposed |
| ERD | Logical/physical data model | TBD |
| API Specification | REST endpoints, schemas, errors, auth | Proposed |
| ADR | Quyết định kiến trúc và lý do | Template needed |
| Coding Guidelines | Coding/naming/project structure | Draft |
| Git Guidelines | Branch/commit/PR/review | Draft |
| QA/Test Plan | Test levels, datasets, acceptance, evidence | Draft |
| Security & Deployment Guide | Security, environments, CI/CD, backup/restore | Draft |
| Operations Runbook | Monitoring, incident, fallback, recovery | TBD |
| Handover & Exit Playbook | Source/config/export/training/exit | TBD |

## 2. Recommended Repository Structure

```text
repository/
├── README.md
├── docs/
│   ├── 01-project-overview.md
│   ├── 02-requirements.md
│   ├── 03-project-planning.md
│   ├── 04-team-responsibilities.md
│   ├── 05-technical-design.md
│   ├── 06-development-standards.md
│   ├── 07-project-management-tools.md
│   ├── 08-quality-assurance-testing.md
│   ├── 09-security-deployment.md
│   ├── 10-documentation-index.md
│   ├── adr/
│   │   └── 000-template.md
│   ├── api/
│   ├── diagrams/
│   ├── test-evidence/
│   └── runbooks/
├── apps/
├── services/
├── migrations/
├── tests/
└── .github/
```

## 3. README.md – Minimum Contents

- Project name and short description.
- Problem/objective.
- Scope and out-of-scope.
- Architecture overview and diagram.
- Technology stack (approved, not merely proposed).
- Prerequisites.
- Local setup and run instructions.
- Environment variables (names only; no secrets).
- Database migration and seed instructions.
- Test/lint commands.
- API docs link.
- Branch/PR workflow.
- Security and data handling notes.
- Known limitations.
- Maintainers/contact route.

## 4. SRS – Minimum Contents

1. Purpose and document conventions.
2. Product scope and boundaries.
3. Stakeholders and user classes.
4. Business requirements.
5. Functional requirements with IDs.
6. Non-functional requirements.
7. External interface requirements.
8. Data requirements and source authority.
9. Use cases/user stories.
10. Acceptance criteria.
11. Constraints, assumptions and dependencies.
12. Traceability matrix.
13. Open questions and change history.

## 5. Architecture Document – Minimum Contents

- Context and architecture drivers.
- Design principles.
- System context.
- Component/module boundaries.
- Data flow: import, question/answer, referral, withdrawal.
- Security boundaries and trust zones.
- Deployment topology.
- Data stores and external providers.
- Failure modes/fallback.
- Performance/cost limits.
- Architecture decisions and trade-offs.

## 6. ERD – Minimum Contents

- Entity names and descriptions.
- PK/FK and cardinality.
- Field names/types/nullability.
- Unique/index constraints.
- Version/effective-date model.
- Audit/retention rules.
- Migration ownership.
- Data classification.
- No customer-record tables in base scope unless O1 separately approved.

## 7. API Specification – Minimum Contents

- API version and base path.
- Authentication/authorization.
- Endpoint method/path/description.
- Request/response schemas.
- Error codes and examples.
- Pagination/filtering.
- Idempotency/retry behavior.
- Rate/cost limits.
- Audit behavior.
- OpenAPI/Swagger generation.
- Deprecation/versioning policy.

## 8. ADR Template

```markdown
# ADR-NNN: <Decision title>

- Status: Proposed | Accepted | Rejected | Superseded
- Date: YYYY-MM-DD
- Owners: <names/roles>

## Context
<Problem and constraints>

## Decision
<Decision taken>

## Options Considered
1. <Option A>
2. <Option B>

## Consequences
- Positive:
- Negative:
- Risks:

## Evidence
<PoC, test, cost, privacy/security review>

## Related
<Jira issues, PRs, requirements, other ADRs>
```

## 9. Documentation Governance

- Tài liệu phải có owner, version, status, last updated và reviewer.
- Requirement changes phải cập nhật traceability.
- Architecture changes quan trọng cần ADR.
- API contract thay đổi phải cập nhật OpenAPI và tests.
- Policy content thuộc quyền Policy Owner; tài liệu kỹ thuật không thay thế policy source.
- Tài liệu có dữ liệu hạn chế phải lưu trong nơi được cấp quyền, không mặc định public trong GitHub.
- Không ghi secrets, customer data hoặc thông tin cá nhân không cần thiết.
- Handover phải gồm code/configuration/mappings/deployment/restore/training/exit artifacts được đặt hàng.

## 10. Documentation Release Checklist

- [ ] README setup đã được kiểm thử bởi thành viên khác.
- [ ] Requirements có ID và traceability.
- [ ] Architecture/ADR phản ánh implementation thực tế.
- [ ] ERD và migration đồng bộ.
- [ ] OpenAPI khớp API thực tế.
- [ ] Coding/Git guidelines được team chấp thuận.
- [ ] QA evidence có thể truy xuất.
- [ ] Deployment/restore/exit guide đã được chạy thử.
- [ ] Tài liệu handover được owner chấp nhận.

## 11. Source Notes

RFP trang 12–13 (roles/deliverables), trang 8 (work packages), trang 22 (restore/exit tests). README/SRS/ADR conventions là đề xuất tài liệu dự án, không phải format bắt buộc trong RFP.
