# 06. Development Standards – Quy chuẩn phát triển

> **Phiên bản:** 0.1 – Team standard proposal  
> Áp dụng cho toàn bộ source code và tài liệu kỹ thuật trong repository.

## 1. Coding Convention

### Python
- Tuân thủ PEP 8; dùng formatter/linter được pin trong project config (ví dụ Ruff).
- Type hints cho public functions và service boundaries.
- Hàm/class có trách nhiệm rõ, tránh module quá lớn.
- Không hard-code secrets, URLs môi trường hoặc policy critical values.
- Không bắt exception chung chung rồi bỏ qua.
- Không dùng model-generated value làm nguồn sự thật cho critical fields.

### TypeScript/React
- Bật TypeScript strict mode nếu khả thi.
- Component nhỏ, có props/type rõ ràng.
- Tách UI, state và API client.
- Validate response từ API tại boundary.
- Không lưu token nhạy cảm trong local storage nếu có giải pháp session an toàn hơn.

### General
- Ưu tiên code dễ đọc, testable, observable.
- Không commit dead code, debug prints hoặc commented-out blocks không cần thiết.
- Dependency mới phải có lý do và được review.
- Không đưa dữ liệu thật/nhạy cảm vào fixture công khai.

## 2. Naming Convention

| Thành phần | Quy ước | Ví dụ |
|---|---|---|
| Python module/file | `snake_case` | `policy_resolver.py` |
| Python function/variable | `snake_case` | `resolve_effective_policy()` |
| Python class | `PascalCase` | `PolicyResolver` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_CONTEXT_CHARS` |
| TypeScript variable/function | `camelCase` | `getPolicyVersion()` |
| React component | `PascalCase` | `PolicyEvidencePanel` |
| Database table/column | `snake_case` | `policy_versions` |
| API path | lowercase plural nouns | `/api/v1/policies` |
| Environment variable | `UPPER_SNAKE_CASE` | `DATABASE_URL` |
| Test | descriptive `test_...` | `test_withdrawn_policy_is_not_retrieved` |

## 3. Project Structure – Proposal

```text
songnhat-crm-assistant/
├── apps/
│   ├── api/
│   └── web/
├── packages/
│   └── shared-contracts/
├── services/
│   ├── knowledge/
│   ├── policy/
│   ├── retrieval/
│   ├── answering/
│   ├── referral/
│   └── audit/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── acceptance/
│   ├── security/
│   └── fixtures/
├── docs/
│   ├── adr/
│   ├── diagrams/
│   ├── api/
│   └── runbooks/
├── scripts/
├── .github/
│   └── workflows/
├── .env.example
├── .gitignore
├── README.md
└── pyproject.toml
```

Cấu trúc cuối cùng do Tech Lead chốt bằng ADR. Không bắt buộc giữ nguyên nếu repository dùng monorepo khác.

## 4. Git Workflow

### Branches

- `main`: stable/release branch; protected.
- `develop`: integration branch nếu team chọn GitFlow.
- `feature/SON-123-short-description`
- `fix/SON-123-short-description`
- `hotfix/SON-123-short-description`
- `docs/SON-123-short-description`
- `test/SON-123-short-description`

Không push trực tiếp vào `main`. Nếu không dùng `develop`, feature/fix PR có thể merge vào `main` theo chính sách release đã thống nhất.

### Branch lifecycle

1. Jira Issue được tạo và đủ Acceptance Criteria.
2. Tạo branch từ base branch mới nhất.
3. Code và test cục bộ.
4. Commit theo convention.
5. Push branch và mở PR.
6. CI chạy; reviewer kiểm tra.
7. Resolve comments và cập nhật test.
8. Merge theo branch protection.
9. Jira được cập nhật kèm PR/test evidence.
10. Xóa branch sau merge nếu không cần giữ.

## 5. Commit Convention

Format:

```text
<type>(<scope>): <description> [SON-123]
```

Types:
- `feat`: feature
- `fix`: bug fix
- `docs`: documentation
- `refactor`: code restructuring
- `test`: tests
- `chore`: tooling/config
- `perf`: performance
- `security`: security-related change

Examples:

```text
feat(retrieval): add policy passage search [SON-101]
fix(policy): reject withdrawn version [SON-115]
test(answer): cover missing footnote case [SON-121]
docs(api): document question endpoint [SON-130]
```

Tránh commit message chung chung như `update`, `final`, `fix bug`, `done`.

## 6. Pull Request Standard

PR phải có:
- Jira Issue Key/link.
- Purpose và scope.
- Summary of changes.
- Test plan và kết quả.
- Screenshot/video cho UI change nếu phù hợp.
- Migration/config/security impact.
- Known limitations và follow-up.
- Checklist DoD.

Quy tắc:
- Author không tự approve PR của mình.
- Ít nhất 1 reviewer khác; critical/security/data change có reviewer chuyên trách.
- CI phải pass.
- Không merge khi unresolved critical review comment.
- PR lớn nên chia nhỏ.
- Không squash/rebase/force-push gây mất lịch sử của người khác nếu chưa thống nhất.

## 7. Code Review Checklist

- [ ] Đúng Jira requirement và Acceptance Criteria.
- [ ] Không mở rộng scope trái phép.
- [ ] Code dễ đọc, không duplicate không cần thiết.
- [ ] Input validation và error handling đầy đủ.
- [ ] Authorization kiểm tra phía server.
- [ ] Không log secrets/PII không cần thiết.
- [ ] Tests bao phủ happy path và negative path.
- [ ] Policy date/scope/version/withdrawal được kiểm tra nếu liên quan.
- [ ] Citation trỏ đúng source/version/clause nếu liên quan.
- [ ] Migration/config/documentation cập nhật.
- [ ] Không chứa credential, private data hoặc fixture trái phép.

## 8. Error Handling

- Dùng error codes ổn định.
- Phân biệt validation, authentication, authorization, not found, conflict, rate limit, provider failure và internal error.
- Không expose stack trace hoặc internal secrets cho client.
- Khi provider/model lỗi, fail visibly và cung cấp fallback/manual search/referral.
- Khi evidence thiếu/conflict, trả hold state, không sinh câu trả lời đoán.
- Không retry vô hạn; retries nằm trong usage/cost caps.

## 9. Logging

Log có cấu trúc, tối thiểu:
- timestamp (UTC hoặc chuẩn được thống nhất).
- severity.
- service/environment.
- request/correlation ID.
- actor ID dạng phù hợp với privacy policy.
- event/action/result.
- duration và error code.
- source/version IDs khi cần và được phép.

Không log:
- Password, API key, access token.
- Full customer dossier.
- Nội dung cá nhân không cần thiết.
- Prompt chứa secret hoặc source restricted nếu chưa được phê duyệt.

## 10. Definition of Done (DoD)

- [ ] Acceptance Criteria đạt.
- [ ] Code committed/pushed.
- [ ] PR được review và merge.
- [ ] Unit/integration/API tests liên quan pass.
- [ ] Không còn critical/high defect chưa được xử lý hoặc chấp nhận có văn bản.
- [ ] Documentation/ADR/migration được cập nhật.
- [ ] Security/privacy impact được xem xét.
- [ ] Jira có trạng thái và evidence link chính xác.

## 11. Repository Protection

- Protect `main` và `develop` (nếu dùng).
- Require PR review và required status checks.
- Hạn chế force push/deletion.
- Dùng secret scanning/dependency scanning nếu có.
- `.env` nằm trong `.gitignore`; chỉ commit `.env.example` với placeholder.
- Repository visibility và quyền collaborator theo nguyên tắc least privilege.
