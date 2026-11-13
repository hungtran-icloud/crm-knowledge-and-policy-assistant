# 03. Project Planning – Lập kế hoạch

> **Phiên bản:** 0.1 – Planning baseline proposal  
> **Lưu ý:** Lịch RFP là cơ sở. Sprint là chu kỳ quản lý nội bộ; Release Gate là mốc nghiệm thu, không đồng nghĩa một-một với Sprint.

## 1. Planning Principles

1. G0 là readiness gate sau Discovery, trước khi cam kết build.
2. G1–G4 là các release gates của RFP.
3. Không rút ngắn 20 business days supervised pilot.
4. Không âm thầm mở rộng scope; scope change cần requirement được duyệt, price, owner, rights review và test impact.
5. Các giả định volume/effort phải được xác minh tại G0.
6. Dùng Jira để theo dõi tiến độ và GitHub để truy vết code/PR.

## 2. Project Timeline

RFP schedule:
- Discovery: tuần 1–2.
- Implementation tuần 1–3: imports, permissions, policy selection, original references, exact fields; G1.
- Implementation tuần 4: answer/referral workspace, independent evaluation, challenges, training; G2 nếu pass.
- Implementation tuần 5–8: tối thiểu 20 business days supervised use.
- Implementation tuần 9–10: G3 decision, affected retests, restore/exit tests, training và G4.

> Mốc tuần là sequence dự kiến trong RFP. Ngày lịch cụ thể phải được lập sau khi xác định ngày khởi động, ngày làm việc, ngày nghỉ và availability của Policy Owners.

## 3. Milestones & Release Gates

| Milestone | Gate | Điều kiện đạt | Evidence |
|---|---|---|---|
| M0 Discovery ready | G0 | Families, approved sample, curation capacity, rights, authority, recurring tasks, priced route comparison được xác nhận | Discovery report, source register, G0 decision |
| M1 Controlled offline | G1 | Corpus/field rows approved; imports reconcile; permissions, dates, conflicts, original references verified | Import report, permission/date/conflict tests |
| M2 Supervised use | G2 | Independent quality/challenge gates pass; no critical defect; legal deployment review complete; owners trained; fallback ready | Evaluation report, legal review, training/fallback evidence |
| M3 Pilot acceptance | G3 | ≥20 business days supervised use; effort/use/cost report; acceptance decision | Pilot report, independent scores, value case |
| M4 Handover | G4 | Restore/deletion/exit tests pass; code/config/docs/training accepted | Handover pack, restore/exit test results |

## 4. Sprint Planning – Internal Proposal

Đề xuất tổ chức bốn Sprint triển khai, nhưng không ép mỗi Gate thành một Sprint:

| Sprint | Window tham chiếu | Goal | Workstreams |
|---|---|---|---|
| Sprint 1 | Implementation weeks 1–3 | Controlled offline | Data/KB, import, policy metadata/version, permissions, source refs, reconciliation |
| Sprint 2 | Implementation week 4 | Supervised-use readiness | RAG/workspace, citations, applicability, missing facts, referral, QA, security/legal review |
| Sprint 3 | Implementation weeks 5–6 | Pilot observation – part 1 | Supervised use, issue triage, measurement, controlled fixes |
| Sprint 4 | Implementation weeks 7–8 | Pilot observation – part 2 | Complete ≥20 business days, measure effort/use/quality/cost |
| Finalization | Implementation weeks 9–10 | Acceptance & handover | G3 decision, retests, restore/exit, training, G4 |

**Cảnh báo lịch:** Sprint 3 và Sprint 4 chỉ là cách chia nội bộ giai đoạn quan sát. Nếu ngày nghỉ/volume thấp khiến chưa đủ 20 ngày làm việc, pilot phải kéo dài. Không được đánh dấu G3 chỉ vì hết Sprint 4.

## 5. Task Breakdown – Work Breakdown Structure

### EP01 – Discovery & Requirement Analysis
- Inventory current procedures and source systems.
- Profile representative historical questions/observation.
- Confirm families, owners, substitutes and authority matrix.
- Rights and source completeness review.
- Baseline effort/use measurement.
- Compare searchable library/configured product/custom route.
- Approve scope, assumptions, costs and G0.

### EP02 – Knowledge Base & Data Import
- Define passage and critical-field CSV schemas.
- Build validators, manifest, quarantine and reconciliation.
- Preserve original references and stable IDs.
- Implement idempotent imports, late-batch protection and tombstones.
- Test batch, snapshot and withdrawal behavior.

### EP03 – Policy Management & Version Control
- Policy lifecycle and publication states.
- Effective interval and governing-date logic.
- Authority/scope metadata.
- Supersession and conflict detection.
- Critical fields typed schema and deterministic rendering.
- Change impact and stale-answer handling.

### EP04 – AI Retrieval & Question Answering
- Vietnamese normalization and approved synonyms.
- Permission/date/scope filtering before retrieval.
- Retrieval and reranking evaluation.
- Answer package assembly with citations.
- Hold/clarification behavior.
- Prompt injection/untrusted content robustness.

### EP05 – User Interface & Referral
- Chat and policy evidence workspace.
- Clause/page reference navigation and highlight.
- Structured field display.
- Missing-information display.
- Local referral record and status.

### EP06 – Security, Privacy & Governance
- RBAC and source-level access checks.
- Secrets/environment management.
- Audit events and retention design.
- Provider/location/retention assessment.
- AI classification rationale and responsibility matrix.
- Incident/change process and fallback.

### EP07 – Testing, Evaluation & Acceptance
- Test strategy and test data governance.
- 60 dev / 40 validation / 100 sealed task partitions.
- 80 constructed challenges.
- Independent review and scoring.
- Performance, import, dates, fields, withdrawal, restore tests.
- Pilot effort/use/cost report.

### EP08 – Deployment, Monitoring & Handover
- Build/deploy environments and CI/CD.
- Monitoring and cost meters.
- Backup/restore and recovery tests.
- Exit/export and deletion tests.
- Documentation, training and handover.

## 6. Priority

| Priority | Ý nghĩa | Quy tắc |
|---|---|---|
| P0 – Critical | An toàn, quyền, policy authority, false approval, withdrawn policy | Block release nếu chưa đạt |
| P1 – High | Chức năng cốt lõi cần cho Gate hiện tại | Ưu tiên trong Sprint |
| P2 – Medium | Cải thiện usability/operation không block gate | Làm sau P0/P1 |
| P3 – Low | Nice-to-have/option | Không tự đưa vào base scope |

## 7. Deliverables

| ID | Deliverable | Mốc |
|---|---|---|
| DEL-01 | Question inventory, baseline, source register, authority/date matrix, scope, field dictionary, deployment review, acceptance plan | G0 |
| DEL-02 | Two import validators, policy selection, cited workspace, exact field display, local referral, publication/withdrawal | G1/G2 |
| DEL-03 | Reconciliation, independent scores, control results, effort/use/cost report, updated value case | G3 |
| DEL-04 | Commissioned code, mappings, configuration, deployment/restore guides, lawful test fixtures, training, exit playbook | G4 |
| DEL-05 | Commercial response: itemized discovery, curation, build, imports, licenses, hosting, model/retrieval, tests, training, maintenance, support, options, exit; 3-year VND TCO/VAT | Procurement |
| DEL-06 | Operating terms: service hours, response/recovery, provider dependencies/locations/subprocessors, support, warranty, renewal and exit | Procurement |

## 8. Risk Management

| ID | Risk | Impact | Mitigation / Trigger |
|---|---|---|---|
| R-01 | Không có Policy Owner hoặc authority matrix | Không xác định được rule đúng | Không qua G0/G1 với family chưa có owner |
| R-02 | Source thiếu footnote/table/diagram | Trả lời sai critical rule | Quarantine/hold; owner bổ sung bản gốc |
| R-03 | Policy version/date conflict | Dùng sai policy | Explicit governing-date logic; hold conflicts |
| R-04 | Data rights/privacy chưa rõ | Rủi ro pháp lý/bảo mật | Không đưa real data vào trước review |
| R-05 | API provider xử lý dữ liệu không phù hợp | Rủi ro provider/transfer/retention | Thẩm định provider và data flow; cân nhắc local/hybrid |
| R-06 | Hallucination/fabricated citation | Sai hướng dẫn | Deterministic fields, citations, sealed tests, zero critical failures |
| R-07 | Scope creep (CRM integration/OCR/automation) | Trễ và vượt chi phí | Change control, separate quote and tests |
| R-08 | Pilot không đủ task/usage | Không đo được value | Profile historical weeks; extend observation if needed |
| R-09 | Cost vượt cap | TCO không khả thi | Meter attempts/failures/retries; visible holds |
| R-10 | Key person dependency | Chậm review/approval | Owner substitutes, documented handover |
| R-11 | Restore làm sống lại withdrawn/deleted data | Data/security failure | Replay deletion/withdrawal/rights state before access |
| R-12 | Sealed test leakage | Kết quả acceptance không độc lập | Access control; independent reviewer; fresh retest |

## 9. Change Control

Mọi thay đổi scope phải ghi:
- Requirement/Issue ID và lý do.
- Business owner và người phê duyệt.
- Tác động đến cost, timeline, architecture, privacy/rights.
- Gate và test bị ảnh hưởng.
- Quyết định: approve / defer / reject.
- Phiên bản tài liệu và ngày hiệu lực.

## 10. Jira Planning Fields

Mỗi Jira Issue nên có: Epic, Sprint, Release Gate, Workstream, Priority, Assignee, Estimate, Acceptance Criteria, Dependencies, Due Date (nếu có), Evidence Link.

## 11. Source Notes

RFP trang 4 (readiness/schedule assumptions), trang 8 (work packages), trang 9–13 (acceptance, gates, schedule, team, deliverables), trang 22–24 (operational/value tests).
