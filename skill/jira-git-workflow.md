# SKILL — Jira + Git Workflow

> Hướng dẫn tích hợp Jira và Git cho dự án CKPA.
> Đọc cùng [jira-playbook.md](../docs/jira-playbook.md) và [git-playbook.md](../docs/git-playbook.md).

## Tạo branch từ Jira issue

```bash
# Lấy issue key từ Jira (vd: CKPA-123)
git switch -c feature/CKPA-123-short-description
```

## Commit convention

```
<type>(<scope>): <mô tả> [CKPA-123]
```

Ví dụ:
```
feat(ingestion): add CSV quarantine isolation [CKPA-21]
fix(retrieval): filter withdrawn passages before ranking [CKPA-45]
test(answer): add citation validation edge cases [CKPA-67]
```

## Quy trình PR

1. Tạo branch từ `main` hoặc `develop` (theo quy ước nhóm).
2. Commit thay đổi, chạy `make lint test` trước push.
3. Mở PR với title `[CKPA-123] <mô tả>`, dùng template trong git-playbook.
4. Reviewer gắn `[blocking]` hoặc `[suggestion]`.
5. Merge sau khi CI pass và không còn comment blocking.

## Checklist nhanh

- [ ] Branch đúng convention.
- [ ] Commit gắn CKPA issue key.
- [ ] Không commit secret/dữ liệu thật.
- [ ] Đã chạy lint + test.
- [ ] PR có evidence/cách test.
