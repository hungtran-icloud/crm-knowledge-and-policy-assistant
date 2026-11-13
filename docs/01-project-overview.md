# 01. Project Overview – Tổng quan dự án

> **Dự án:** SongNhat CRM Knowledge & Policy Assistant  
> **Tài liệu:** Project Overview  
> **Phiên bản:** 0.1 – Draft for team review  
> **Cơ sở:** SongNhat CRM Knowledge and Policy RFP, phát hành trong bộ hồ sơ dự án.

## 1. Project Name – Tên dự án

**SongNhat CRM Knowledge & Policy Assistant**  
Trợ lý tri thức và chính sách CRM SongNhat.

## 2. Project Description – Mô tả dự án

Xây dựng một trợ lý nội bộ hỗ trợ nhân viên tra cứu các quy trình CRM đã được phê duyệt, xác định chính sách/phiên bản áp dụng, hiểu thông tin cần cung cấp và tìm đúng tuyến phê duyệt hoặc Policy Owner. Hệ thống hỗ trợ tìm kiếm tiếng Việt và đưa ra giải thích có trích dẫn chính xác đến điều khoản, tài liệu và phiên bản nguồn.

Hệ thống là công cụ hỗ trợ tra cứu và hướng dẫn. Quyền phê duyệt, quyết định nghiệp vụ và thực thi vẫn thuộc về Policy Owner, người có thẩm quyền và các hệ thống hiện hữu.

## 3. Problem Statement – Vấn đề cần giải quyết

Các vấn đề cần được xác minh trong Discovery:

- Nhân viên có thể mất thời gian tìm kiếm quy trình và xác định phiên bản chính sách đúng.
- Cách giải thích quy trình có nguy cơ không đồng nhất giữa nhân viên.
- Việc xác định thông tin còn thiếu, điều kiện áp dụng, ngoại lệ và tuyến chuyển cấp có thể chưa thuận tiện.
- Nguồn chính sách có thể có nhiều phiên bản, ngày hiệu lực, chủ sở hữu hoặc quyền truy cập khác nhau.
- Câu trả lời không có trích dẫn rõ ràng khiến người dùng khó kiểm tra căn cứ.

RFP xác định mục tiêu giảm thời gian tìm kiếm lặp lại và sự không nhất quán trong giải thích quy trình. Mức giảm sự cố tuân thủ, churn hoặc mất doanh thu chưa được chứng minh và không được xem là lợi ích đã đạt.

## 4. Project Objectives – Mục tiêu dự án

1. Tổ chức kho tri thức từ các quy trình/chính sách được phê duyệt.
2. Quản lý nguồn gốc, chủ sở hữu, người phê duyệt, phiên bản, trạng thái xuất bản và thời gian hiệu lực.
3. Hỗ trợ tìm kiếm câu hỏi tiếng Việt, bao gồm thiếu dấu, từ viết tắt CRM và thuật ngữ tiếng Anh chuyên ngành.
4. Trả lời có căn cứ: hiển thị ngày và phạm vi áp dụng, hướng dẫn, điều khoản chính xác, trường dữ liệu quan trọng, thông tin còn thiếu và tuyến referral.
5. Kiểm soát quyền truy cập, xung đột chính sách, chính sách bị thu hồi và nội dung chưa được phê duyệt.
6. Đánh giá chất lượng, effort, mức sử dụng và chi phí trong pilot có giám sát.
7. Bàn giao mã nguồn được đặt hàng, cấu hình, tài liệu, hướng dẫn khôi phục và quy trình exit.

## 5. Target Users – Đối tượng sử dụng

| Nhóm | Vai trò dự kiến |
|---|---|
| Nhân viên được cấp quyền | Tra cứu quy trình, xem căn cứ và thông tin còn thiếu |
| Policy Owner | Xác nhận thẩm quyền, nội dung, ngoại lệ, ngày hiệu lực và referral |
| Knowledge/Data Steward | Chuẩn bị nguồn, metadata, import, version và withdrawal |
| Publisher/Approver | Phê duyệt và xuất bản nội dung theo phân quyền |
| Administrator | Quản trị người dùng, vai trò và cấu hình kỹ thuật |
| Privacy/Security/Legal Owner | Đánh giá quyền xử lý, bảo mật và tính áp dụng pháp lý |
| Project/Supplier Team | Phát triển, kiểm thử, triển khai và bàn giao |

Số lượng người dùng và vai trò cuối cùng phải được xác nhận tại G0. RFP đưa ra giả định lập kế hoạch ban đầu là 20 người dùng được định danh và 5 phiên đồng thời.

## 6. Scope – Phạm vi dự án

### 6.1 Phạm vi cơ sở (Base Scope)

- Ba nhóm chính sách dự kiến, cần xác nhận trong Discovery:
  1. Quy trình báo giá và phê duyệt thương mại.
  2. Xử lý thông tin khách hàng.
  3. Tiếp nhận và chuyển tuyến yêu cầu dịch vụ/bảo hành.
- Kho văn bản/điều khoản đã được phê duyệt và các trường chính sách có cấu trúc.
- Import qua hai schema CSV UTF-8 cho approved passages và critical policy fields.
- Metadata về nguồn, chủ sở hữu, người phê duyệt, version, publication state, effective interval, scope, audience và supersession.
- Tìm kiếm tiếng Việt và câu trả lời có trích dẫn.
- Kiểm tra quyền, trạng thái xuất bản, ngày hiệu lực và phạm vi trước khi hiển thị.
- Xử lý thiếu dữ kiện, xung đột và chuyển Policy Owner.
- Publication, scheduled effectiveness, withdrawal, change impact, audit, evaluation, recovery và portable exit.
- UI làm việc hiển thị câu hỏi, ngày/phạm vi, hướng dẫn, trích dẫn, trường cấu trúc, thông tin thiếu và referral.

### 6.2 Các giả định quy mô cần xác nhận tại G0

RFP đưa ra các giả định bid basis, không phải dữ liệu thực tế đã xác nhận:

- Tối đa 30 tài liệu được phê duyệt.
- 300 passages đã curate.
- 50 critical field rows.
- 20 named users, 5 concurrent sessions.
- Một batch/ngày/schema đang hoạt động, tối đa 500 rows thay đổi/ngày.
- Tối đa 1.000 answer packages/tháng, tính cả hold và failure.

Không tạo thêm quy tắc nghiệp vụ chỉ để đạt các giới hạn số lượng này.

## 7. Out of Scope – Ngoài phạm vi cơ sở

Các nội dung sau không thuộc base scope, trừ khi có phê duyệt thay đổi phạm vi và kiểm thử/ngân sách riêng:

- Import hồ sơ khách hàng, mailbox history hoặc full customer dossiers.
- O1 selected CRM context: chỉ xem xét như option riêng, cần xác minh identity, permissions, lawful processing và additional value.
- Live CRM/repository connectors.
- OCR, audio, ngôn ngữ bổ sung.
- Tự động gửi email/tin nhắn, tạo CRM task hoặc writeback.
- Tự động phê duyệt giao dịch/ngoại lệ hoặc thực thi workflow.
- Quyết định eligibility, quyền tiết lộ dữ liệu, entitlement bảo hành hay hướng dẫn sửa chữa thiết bị.
- Tư vấn pháp lý/thuế hoặc chứng nhận tuân thủ.
- Fine-tuning LLM, nếu chưa có lý do và phê duyệt riêng. RFP không bắt buộc fine-tuning.

## 8. Expected Outcomes – Kết quả mong đợi

- Kho tri thức được phê duyệt, có thể truy vết nguồn và phiên bản.
- Import có reconciliation, quarantine và kiểm soát withdrawal.
- Workspace trả lời tiếng Việt có trích dẫn điều khoản áp dụng.
- Cơ chế hold/clarification/referral khi thiếu nguồn, xung đột hoặc không đủ căn cứ.
- Báo cáo kiểm thử độc lập và kết quả pilot.
- Bộ tài liệu, code/configuration được đặt hàng, hướng dẫn deployment/restore, đào tạo và exit playbook.

Các mục tiêu nghiệm thu chất lượng cụ thể được ghi trong `02-requirements.md`.

## 9. Nguyên tắc vận hành

- RFP và hợp đồng/addenda được duyệt là căn cứ xác định yêu cầu.
- Policy Owner giữ quyền quyết định nội dung chính sách.
- AI chỉ giải thích bằng chứng được phép truy xuất; không tự tạo luật/quy tắc.
- Không có căn cứ hoặc có xung đột: hold kết luận liên quan và referral.
- Không dùng dữ liệu khách hàng trong base scope.
- Historical answers phải hiển thị ngày và không được trình bày như hướng dẫn hiện hành.

## 10. Open Questions cần chốt tại G0

- Danh sách policy families chính thức và Policy Owner/substitute.
- Hệ thống CRM hiện tại, khả năng export và quyền truy cập.
- Danh mục nguồn, quyền sử dụng, phiên bản và ngôn ngữ kiểm soát.
- Câu hỏi thực tế, tần suất, baseline effort và nhóm người dùng pilot.
- Quy tắc governing date, authority matrix và xử lý xung đột.
- Phương án triển khai/API/local/hybrid sau đánh giá privacy, provider, data location, retention và cost.
- Ngân sách, nhân lực curation, chi phí 3 năm và điều kiện support.

## 11. Source Notes

Tóm lược theo RFP: trang 1–4 (mục tiêu, base scope, pilot assumptions), trang 5–8 (authority, answer package, knowledge operations, work packages), trang 10–13 (acceptance, gates, schedule, ownership, deliverables). Các giới hạn cần được xác nhận tại G0.
