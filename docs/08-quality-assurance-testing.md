# 08. Quality Assurance & Testing – Kiểm thử

> **Phiên bản:** 0.1 – QA strategy proposal  
> Quality gates và acceptance thresholds lấy từ RFP; test cases cụ thể phải được Policy Owners/independent reviewers xác nhận.

## 1. Testing Principles

- Test từ đầu, không đợi đến cuối dự án.
- Mọi requirement quan trọng có test ID và evidence.
- Tách development, validation và sealed acceptance sets.
- Developer không tune trên sealed acceptance cases.
- Independent reviewers không phải người đã tune hệ thống.
- Critical control failure block release.
- Citation presence không đồng nghĩa citation support; reviewer phải kiểm tra nội dung claim và clause.

## 2. Test Levels

| Test type | Mục tiêu | Ví dụ |
|---|---|---|
| Unit Testing | Kiểm tra logic module nhỏ | date resolver, permission filter, critical field renderer |
| Integration Testing | Kiểm tra tương tác module | import → registry → index; withdrawal → cache invalidation |
| API Testing | Contract, validation, auth và error behavior | POST question, unauthorized source |
| End-to-End Testing | Luồng người dùng hoàn chỉnh | hỏi → xem answer → mở citation → referral |
| Performance Testing | Latency, concurrency, import throughput | p95 response với 5 concurrent users |
| Security Testing | RBAC, access leakage, prompt injection, secrets | user không được xem restricted passage |
| Regression Testing | Không làm hỏng chức năng đã đạt | policy withdrawal/date tests sau mỗi release |
| Acceptance Testing | Đạt RFP criteria | sealed tasks, pilot metrics, G3 evidence |

## 3. Test Dataset

Theo RFP:
- 200 permitted real question tasks:
  - 60 development.
  - 40 validation.
  - 100 sealed acceptance.
- 80 constructed challenges.
- Hai Policy Reviewers thống nhất expected clauses, dates, scope, exceptions và referral labels.
- Related variants và records phải nằm cùng partition để tránh leakage.
- Nếu dữ liệu thực tế ít, phải thu hẹp scope hoặc kéo dài collection; không tự tạo dữ kiện rồi xem như dữ liệu thật.

## 4. Challenge Categories

- Future/obsolete policies.
- Threshold boundaries.
- Missing footnotes.
- Contract conflicts.
- Wrong role.
- CRM note overrides.
- Prompt injection.
- Withdrawal during generation.
- Missing/ambiguous date.
- Vietnamese missing diacritics and mixed English terms.
- Rights/access/withdrawal challenges.

RFP yêu cầu thêm 40 Vietnam-oriented challenges: 10 language, 10 dates/scope, 10 threshold/exception, 10 rights/withdrawal.

## 5. Acceptance Targets

| Metric | Target |
|---|---:|
| Unauthorized disclosure | 0 observed |
| Fabricated critical field | 0 |
| False approval | 0 |
| Current guidance from withdrawn/future policy | 0 |
| Correct version/scope/governing date on sealed answerable tasks | ≥95% |
| Material claims supported by applicable clauses | ≥95% |
| Required clauses/exceptions included | ≥90% |
| Fabricated citations | 0 |
| Retrieval recall@5 | ≥90% |
| Answerable tasks useful with minor edits | ≥80% |
| Unanswerable tasks materially unsupported | ≤5% |
| Supervised pilot | ≥20 business days |
| Staff effort | Target ≥20% lower mean total effort, quality equal/better |

## 6. Test Case Template

| Field | Description |
|---|---|
| Test ID | Unique ID, e.g. `TC-POL-001` |
| Requirement ID | Linked requirement |
| Scenario | Test purpose |
| Preconditions | User role, policy state, source/version |
| Input | Question/data |
| Governing date/scope | Expected context |
| Expected evidence | Clause/version/field |
| Expected behavior | Answer/clarify/hold/referral |
| Actual result | Observed output |
| Status | Pass/Fail/Blocked |
| Severity | Critical/High/Medium/Low |
| Reviewer | Tester/independent reviewer |
| Evidence | Screenshot/log/report link |

## 7. Representative Test Cases

| ID | Scenario | Expected |
|---|---|---|
| TC-001 | General CRM procedure question | Current approved policy, exact citations, missing info |
| TC-002 | Dated transaction | Correct historical version and visibly dated answer |
| TC-003 | Future policy scheduled | Not used as current policy |
| TC-004 | Withdrawn policy | Not retrieved/served as current |
| TC-005 | Conflicting contract | Hold conclusion and refer owner |
| TC-006 | Old CRM note | Not treated as general policy |
| TC-007 | Missing critical footnote | Hold affected threshold |
| TC-008 | Wrong user role | No unauthorized evidence disclosure |
| TC-009 | Prompt injection in source | Treat as untrusted data |
| TC-010 | Withdrawal while generation paused | Withhold answer after withdrawal acknowledgment |
| TC-011 | Threshold below/equal/above | Exact approved operator/value/unit/role |
| TC-012 | Vietnamese missing diacritics | Retrieval evaluated against expected evidence |
| TC-013 | Partial/late import batch | Reconciliation correct; no overwrite of newer version |
| TC-014 | Retry duplicate import | Idempotent result |
| TC-015 | Restore backup | Replay withdrawal/deletion/current rights before access |

## 8. Performance & Operational Tests

Theo RFP:
- Import 500 changed rows trong 30 phút; reconcile từng row.
- 5 concurrent users; p95 ≤25 seconds trên 100 requests trong context caps.
- Test date boundaries, expired intervals, overlap, backdated corrections.
- Test critical fields below/equal/above boundary, missing unit/currency, exceptions.
- Withdrawal test: pause generation → commit withdrawal/access revocation → acknowledgment → resume; no affected answer may be newly served/reused.
- Test cache cleanup separately.
- Test usage/token/cost caps; không silent truncation hoặc retries ngoài cap.
- Restore target RTO 4 covered hours, RPO 24 hours.
- Proposed availability target 99.5% in contracted service hours; confirm contract.

## 9. Defect Severity

| Severity | Description | Release treatment |
|---|---|---|
| Critical | Unauthorized disclosure, false approval, fabricated critical field, withdrawn/future policy shown current | Release blocker; disable affected path |
| High | Wrong policy/version/citation or major workflow failure | Fix/retest before relevant Gate unless formally scoped out |
| Medium | Non-critical defect with workaround | Prioritize and document |
| Low | Cosmetic/minor usability issue | Backlog with owner |

Không giảm tiêu chí acceptance sau khi biết kết quả sealed test nếu không có quyết định mới được ghi nhận và independent retest.

## 10. Definition of Done for QA

- Test case linked to requirement/Jira.
- Test data permitted and access controlled.
- Expected result reviewed.
- Test executed with evidence.
- Defects recorded and triaged.
- Regression tests pass.
- Critical blockers = 0 for release.
- QA recommendation and limitations documented.

## 11. Source Notes

RFP trang 9–10 (dataset, independent evaluation, acceptance thresholds), trang 20 (worked cases), trang 22 (operational tests), trang 28 (Vietnam challenge fixtures).
