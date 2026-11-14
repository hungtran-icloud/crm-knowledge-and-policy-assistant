# JIRA PLAYBOOK — HƯỚNG DẪN SỬ DỤNG JIRA

> Hướng dẫn cấu trúc công việc, tạo issue, viết mô tả, cập nhật trạng thái và trình bày thông tin trên Jira.

## 1. Jira dùng để làm gì
Jira là nơi ghi nhận và theo dõi công việc. Mỗi issue cần làm rõ: cần làm gì, vì sao, kết quả mong đợi, ai phụ trách, thời hạn và điều kiện hoàn thành.

## 2. Các khái niệm
| Loại | Mục đích | Ví dụ |
|---|---|---|
| Epic | Nhóm phạm vi lớn | EP04 — Retrieval & QA |
| Story | Nhu cầu/kết quả có giá trị với người dùng | Staff can view cited guidance |
| Task | Công việc cụ thể | Prepare import validation |
| Bug | Hành vi sai so với mong đợi | Citation opens wrong page |
| Spike | Nghiên cứu để đưa ra kết luận | Evaluate search options |
| Sub-task | Phần nhỏ thuộc issue cha | Add validation test |

## 3. Trường thông tin nên có
- **Summary:** tiêu đề ngắn, nêu đúng kết quả.
- **Issue Type:** Epic, Story, Task, Bug, Spike hoặc Sub-task.
- **Description:** bối cảnh, mục tiêu, phạm vi, ghi chú.
- **Acceptance Criteria:** điều kiện nghiệm thu kiểm tra được.
- **Priority:** mức ưu tiên.
- **Assignee:** người chịu trách nhiệm chính.
- **Parent/Epic:** issue cha hoặc Epic liên quan.
- **Labels/Components:** nhãn phân loại nếu nhóm sử dụng.
- **Sprint, Due date, Estimate:** điền khi project có quy ước tương ứng.
- **Links/Attachments:** tài liệu và issue liên quan.

## 4. Quy tắc viết Summary
Bắt đầu bằng động từ/kết quả, nêu rõ đối tượng, ngắn gọn. Tránh tiêu đề chung chung.

**Tốt:** `Display source citation in answer panel`; `Fix incorrect page number in citation`.

**Không tốt:** `Update`; `Fix bug`; `Do task`; `Work on chatbot`.

## 5. Template Description
```markdown
## Background
Bối cảnh hoặc lý do cần thực hiện.

## Objective
Kết quả cụ thể cần đạt.

## Scope
- Trong phạm vi:
- Ngoài phạm vi:

## Requirements / Notes
- Yêu cầu 1
- Yêu cầu 2

## Dependencies
- Issue/người cần phối hợp:
- Điều kiện cần có:

## References
- Link tài liệu:
```

## 6. Acceptance Criteria (AC)
AC phải kiểm tra được, tránh câu mơ hồ như “hoạt động tốt”. Có thể dùng checklist:
```markdown
## Acceptance Criteria
- [ ] Điều kiện 1 có thể kiểm tra.
- [ ] Điều kiện 2 có thể kiểm tra.
- [ ] Trường hợp lỗi được mô tả.
```
Hoặc Given/When/Then:
```gherkin
Given <điều kiện ban đầu>
When <hành động>
Then <kết quả mong đợi>
```

## 7. Priority và Status
Priority tham khảo: P0/Highest (khẩn cấp), P1/High (cao), P2/Medium (thường), P3/Low (thấp). Tên thực tế phụ thuộc cấu hình Jira.

Workflow tham khảo: `Backlog → Selected → In Progress → In Review → QA/Verification → Done`. Có thể có `Blocked`, `Rejected`, `Reopened`. Chỉ chuyển Done khi đáp ứng AC.

## 8. Comment cập nhật tiến độ
```markdown
## Progress
- Completed:
- In progress:
- Remaining:

## Blockers
- Vấn đề:
- Cần hỗ trợ từ:

## ETA
- Dự kiến hoàn thành:
```
Comment cần ghi thông tin mới, không lặp lại Description. Khi bị Blocked phải nêu nguyên nhân và điều kiện để tiếp tục.

## 9. Liên kết issue
- `blocks / is blocked by`: issue này chặn issue kia.
- `relates to`: có liên quan.
- `duplicates`: trùng lặp.
Chỉ dùng blocks khi issue kia thực sự không thể tiếp tục trước khi issue này hoàn tất.

## 10. Template Bug
```markdown
## Summary
Mô tả ngắn lỗi.
## Steps to Reproduce
1.
2.
3.
## Expected Result
Kết quả mong đợi.
## Actual Result
Kết quả thực tế.
## Evidence
- Screenshot/log/link:
## Acceptance Criteria
- [ ] Tái hiện được lỗi.
- [ ] Nguyên nhân được xử lý.
- [ ] Kiểm tra xác nhận đã sửa.
```

## 11. Template Spike
```markdown
## Question
Câu hỏi cần nghiên cứu.
## Background
Lý do cần tìm hiểu.
## Options to Evaluate
- Option A:
- Option B:
## Evaluation Criteria
- Tiêu chí 1:
## Expected Output
- Kết luận:
- Ưu/nhược điểm:
- Đề xuất:
- Việc tiếp theo:
```

## 12. Lỗi thường gặp
| Lỗi | Cách sửa |
|---|---|
| Summary mơ hồ | Viết theo hành động + đối tượng |
| Description quá ngắn | Dùng template và nêu phạm vi |
| AC không kiểm tra được | Viết checklist hoặc Given/When/Then |
| Không có Assignee | Gán một owner chính |
| Không cập nhật Blocked | Comment blocker và nhu cầu hỗ trợ |
| Done quá sớm | Chỉ Done khi đủ AC |
| Issue trùng | Tìm kiếm trước khi tạo, liên kết duplicate |

> Tên trường và workflow phải khớp cấu hình Jira thực tế của nhóm.
