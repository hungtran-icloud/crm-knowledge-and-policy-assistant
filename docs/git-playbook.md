# GIT PLAYBOOK — HƯỚNG DẪN GIT & GITHUB

> Hướng dẫn branch, commit, push, đồng bộ code, Pull Request, review và xử lý conflict.

## 1. Khái niệm cơ bản
| Khái niệm | Ý nghĩa |
|---|---|
| Repository | Kho lưu trữ source code |
| Working tree | File đang chỉnh sửa trên máy |
| Staging area | Khu vực chuẩn bị nội dung commit |
| Commit | Một mốc lưu thay đổi |
| Branch | Nhánh phát triển độc lập |
| Remote | Repository từ xa |
| Push | Đẩy commit lên remote |
| Pull | Lấy và tích hợp thay đổi |
| Fetch | Tải thông tin từ remote |
| Merge | Gộp lịch sử hai nhánh |
| Rebase | Đặt lại commit trên base mới |
| Pull Request | Đề xuất tích hợp thay đổi |

## 2. Quy tắc branch
Nhánh chính tham khảo: `main` (ổn định), `develop` (tích hợp nếu nhóm sử dụng). Không code trực tiếp trên nhánh chính.

Format:
```text
<type>/<issue-key>-<short-description>
```
Type: `feature/`, `fix/`, `hotfix/`, `refactor/`, `docs/`, `test/`, `chore/`.

Ví dụ:
```text
feature/SON-123-policy-search
fix/SON-145-citation-page
docs/SON-160-update-readme
test/SON-171-retrieval-evaluation
```
Dùng chữ thường, dấu gạch ngang, mô tả ngắn và Jira key nếu có issue tương ứng.

## 3. Quy trình cơ bản
```bash
git clone <repository-url>
cd <repository-folder>
git status
git fetch origin
git switch develop
git pull origin develop
git switch -c feature/SON-123-policy-search
```
Nếu repository không có `develop`, dùng branch đích nhóm đã thống nhất.

Trước commit:
```bash
git status
git diff
git add <file>
git diff --staged
git commit -m "feat(search): add policy search [SON-123]"
```
Kiểm tra staging để tránh commit nhầm file.

## 4. Commit message
Format đề xuất:
```text
<type>(<scope>): <short-description> [<JIRA-KEY>]
```
Ví dụ:
```text
feat(api): add policy search endpoint [SON-123]
fix(citation): correct source page mapping [SON-145]
test(retrieval): add ranking evaluation cases [SON-171]
docs(readme): update setup guide [SON-160]
```
Type thường dùng: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`.

Một commit nên đại diện cho một thay đổi có ý nghĩa. Tránh `update`, `fix bug`, `done`, `final code`. Không commit secret, token, password hoặc dữ liệu nhạy cảm.

## 5. Push và đồng bộ
```bash
# Push lần đầu
git push -u origin feature/SON-123-policy-search

# Push tiếp theo
git push

# Tải thông tin remote
git fetch origin

# Xem lịch sử
git log --oneline --graph --decorate -15
```
Chỉ pull/rebase/merge theo cách nhóm đã thống nhất.

## 6. Pull Request
Title đề xuất: `[SON-123] Add policy search endpoint`.

Template:
```markdown
## Summary
Mục tiêu thay đổi.

## Changes
- [ ] Thay đổi 1
- [ ] Thay đổi 2

## Related Issue
Closes SON-123

## How to Test
1.
2.

## Evidence
- Screenshot/log/kết quả test:

## Risks / Notes
- Ảnh hưởng hoặc lưu ý:

## Checklist
- [ ] Đã tự review.
- [ ] Đã chạy kiểm tra phù hợp.
- [ ] Không đưa secret/dữ liệu không được phép vào PR.
- [ ] Đã cập nhật tài liệu liên quan nếu cần.
```
PR cần có mục tiêu rõ, phạm vi hợp lý, liên kết issue và cách kiểm tra. Không tự approve PR của mình. Không merge khi CI bắt buộc fail hoặc còn comment chặn chưa xử lý.

## 7. Review và feedback
Reviewer góp ý vào thay đổi cụ thể, nêu lý do và phân biệt lỗi bắt buộc sửa với đề xuất cải thiện. Người tạo PR phản hồi từng ý, sửa hoặc giải thích rõ nếu không đồng ý. Không đóng comment khi vấn đề chưa được giải quyết.

## 8. Merge và conflict
Merge conflict:
```bash
git fetch origin
git merge origin/develop
# sửa các file conflict
git status
git add <resolved-file>
git commit
```
Rebase conflict:
```bash
git fetch origin
git rebase origin/develop
# sửa các file conflict
git add <resolved-file>
git rebase --continue
```
Hủy rebase:
```bash
git rebase --abort
```
Không dùng `git push --force` tùy tiện. Nếu cần cập nhật branch đã rebase, chỉ dùng `--force-with-lease` khi hiểu tác động và đã thống nhất.

## 9. Lệnh thường dùng
```bash
git status
git branch
git switch <branch>
git switch -c <new-branch>
git diff
git add <file>
git diff --staged
git commit -m "message"
git log --oneline --graph --decorate -15
git fetch origin
git push -u origin <branch>
git restore <file>
git restore --staged <file>
```
`git restore <file>` có thể hủy thay đổi chưa commit trong file đó; cần chắc chắn trước khi chạy.

## 10. Lỗi thường gặp
| Lỗi | Cách xử lý |
|---|---|
| Push rejected | Fetch và tích hợp thay đổi remote rồi push lại |
| Merge conflict | Sửa từng vùng conflict, kiểm tra rồi tiếp tục |
| Commit nhầm file | Kiểm tra `git status` và `git diff --staged` trước commit |
| Sai branch | Kiểm tra `git branch` trước khi sửa |
| Không push được | Kiểm tra remote và quyền truy cập |
| Lỡ commit secret | Báo ngay người phụ trách, thu hồi/đổi secret và xử lý lịch sử |
| Rebase đang dở | Dùng `git status`, tiếp tục hoặc abort rebase |

> Branch protection, CI và quyền repository cần đồng bộ với cấu hình GitHub thực tế.
