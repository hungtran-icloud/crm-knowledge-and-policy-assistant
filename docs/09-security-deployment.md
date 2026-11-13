# 09. Security & Deployment – Bảo mật và triển khai

> **Phiên bản:** 0.1 – Security/deployment baseline proposal  
> Phải được Privacy/Security/Legal Owners duyệt trước khi xử lý dữ liệu thật. Tài liệu này không phải ý kiến pháp lý.

## 1. Security Principles

- Least privilege.
- Deny by default.
- Authorization trước retrieval và trước display.
- Tách identity, policy authority và application role.
- Secrets không nằm trong source code, prompts, logs hoặc Jira.
- Imported documents/questions là untrusted data.
- Không cấp unrestricted tools, public web retrieval hoặc credentials trong prompt.
- Fail visibly; giữ manual search/referral fallback.
- Source withdrawal/access revocation phải chặn việc serve/reuse tiếp theo sau acknowledgment.
- Audit đủ để điều tra nhưng không thu thập dữ liệu thừa.

## 2. Authentication & Authorization

### Authentication
- Tích hợp SSO/OIDC nếu hệ thống hiện hữu hỗ trợ và được duyệt.
- Không tự tạo shared account.
- MFA theo policy tổ chức.
- Session expiration và revocation theo identity policy.

### RBAC proposal

| Role | Quyền dự kiến |
|---|---|
| Reader | Hỏi và xem nguồn được phép |
| Policy Owner | Review nội dung thuộc family được giao; ghi nhận quyết định |
| Publisher/Approver | Publish/schedule/withdraw theo quyền được cấp |
| Knowledge Steward | Import, reconcile, quarantine, chuẩn bị metadata |
| Administrator | Quản trị cấu hình và người dùng; không mặc nhiên có quyền phê duyệt policy |
| Auditor/Reviewer | Đọc audit/evaluation theo phạm vi được phép |

Cần xác nhận role compatibility, segregation of duties và quyền truy cập nguồn tại G0.

## 3. Data Classification & Handling

Trước khi import, phân loại:
- Public.
- Internal.
- Confidential/Restricted.
- Personal data (nếu có).

Base scope dùng approved policy text và structured policy fields; không import customer records. O1 selected CRM context là option riêng, cần identity, permissions, lawful processing, field allowlist, freshness và additional-value review.

Không đưa dữ liệu thật vào API provider/local environment trước khi hoàn tất review:
- Purpose and legal role.
- Provider/subprocessor.
- Data location and transfers.
- Retention/deletion.
- Model training/use terms.
- Access, incident and audit.
- Contractual and regulatory requirements.

RFP nhấn mạnh hosting tại Việt Nam và encryption riêng lẻ không chứng minh compliance.

## 4. Secrets Management

- `.env` không commit.
- `.env.example` chỉ có placeholder.
- Dùng GitHub Secrets hoặc secret manager được tổ chức phê duyệt.
- Rotate/revoke credential khi nghi ngờ lộ.
- Không paste API keys vào Jira, chat, prompt hoặc issue.
- Không log authorization headers/token.
- CI secret scanning nếu có.

## 5. Environment Strategy

| Environment | Mục đích | Data |
|---|---|---|
| Local | Developer work | Synthetic/sanitized fixtures |
| Development | Tích hợp chức năng | Synthetic/approved test data |
| Staging | UAT, security, acceptance rehearsal | Permitted test corpus; access controlled |
| Production/Pilot | Supervised internal use | Chỉ dữ liệu được phê duyệt theo deployment review |

Tách credentials, database, indexes, storage và model-provider config theo environment. Không copy production data sang local/staging tùy tiện.

## 6. Docker & Configuration

- Pin base image và dependencies.
- Non-root container user khi phù hợp.
- Không bake secrets vào image.
- Health checks và resource limits.
- Network access tối thiểu.
- Scan image/dependencies.
- Compose dùng cho local development; production deployment theo platform được phê duyệt.
- Configuration qua environment/secret manager.

## 7. CI/CD Pipeline

PR pipeline đề xuất:
1. Checkout.
2. Dependency install from lockfile.
3. Format/lint.
4. Type/static checks.
5. Unit tests.
6. Integration/API tests.
7. Dependency/secret/security scan.
8. Build container.
9. Artifact publish.
10. Deploy to staging (approval-controlled).
11. Smoke tests.
12. Production/pilot deploy after release approval.

Không tự động deploy production khi Gate/approval chưa đạt.

## 8. Database Backup & Recovery

RFP operational targets:
- Recovery Time Objective (RTO): 4 covered hours.
- Recovery Point Objective (RPO): 24 hours.
- Restore thực tế phải được test, không chỉ xác nhận backup job success.
- Replay deletion, withdrawal và current rights state trước khi cho phép access sau restore.
- Backup retention phải được legal/records owner phê duyệt; thời hạn trong RFP là đề xuất vận hành, không tự động là thời hạn pháp định.

## 9. Monitoring & Logging

Theo dõi:
- API latency/error rate.
- Import throughput/reconciliation/quarantine.
- Retrieval/answer/hold/referral rate.
- Model/provider failures and throttling.
- Token/call/cost caps.
- Access denials and suspicious patterns.
- Withdrawal/change propagation.
- Backup/restore status.
- Availability and incident response.

Không log dữ liệu nhạy cảm không cần thiết. Log access phải được kiểm soát.

## 10. Incident & Fallback

Critical defect examples:
- Unauthorized disclosure.
- Fabricated approval/threshold.
- Withdrawn policy shown as current.
- Access revocation not effective.

Khi có critical issue:
1. Disable affected path/feature.
2. Chuyển sang manual search hoặc owner referral.
3. Ghi nhận impact, time, affected sources/users.
4. Notify incident owner theo agreed process.
5. Root cause và remediation.
6. Independent retest trước khi re-enable.

RFP đề xuất acknowledge production critical issue trong 2 covered hours và target containment trong 4 covered hours trong khung service đã thỏa thuận; cần xác nhận hợp đồng.

## 11. Vietnam Governance Review

RFP yêu cầu trước G2 có:
- Dated AI classification rationale.
- Responsibility matrix.
- Documentation/notices.
- Incident and change process.
- Applicable filing/conformity evidence.
- Legal owner approval về applicability và unresolved dependencies.

RFP tham chiếu Personal Data Protection Law 91/2025/QH15, Decree 356/2025/ND-CP, AI Law 134/2025/QH15, Cybersecurity Law 116/2025/QH15, Decree 142/2026/ND-CP và Decision 33/2026/QD-TTg. Legal Owner phải kiểm tra văn bản hiện hành và áp dụng thực tế; tài liệu này không tự kết luận nghĩa vụ pháp lý.

## 12. Deployment Checklist

- [ ] Environment separation.
- [ ] RBAC and source-level permissions tested.
- [ ] Secrets manager configured.
- [ ] Provider/data flow reviewed.
- [ ] AI classification and responsibility review approved.
- [ ] Audit/logging/retention reviewed.
- [ ] CI/CD and rollback documented.
- [ ] Backup/restore tested.
- [ ] Withdrawal/deletion replay tested.
- [ ] Manual fallback and referral ready.
- [ ] Monitoring/cost limits configured.
- [ ] Gate approval recorded.

## 13. Source Notes

RFP trang 5–8 (authority, answer boundaries, withdrawal), trang 10–11 (G2 and critical defects), trang 22 (restore, exit, service targets), trang 25–26 (Vietnam privacy/AI/cybersecurity review).
