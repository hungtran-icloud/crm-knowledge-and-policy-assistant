# TEAM PLAYBOOK — CRM KNOWLEDGE AND POLICY ASSISTANT

> Hướng dẫn phối hợp và bàn giao cho nhóm thực hiện SongNhat CRM Knowledge and Policy Assistant. Dùng cùng RFP và các tài liệu quy trình của dự án; không dùng playbook này để tự đặt hoặc diễn giải thay chính sách của SongNhat.

## MỤC LỤC
1. Phạm vi và nguyên tắc ưu tiên
2. Vai trò và trách nhiệm
3. Quy trình giao việc và các cổng nghiệm thu
4. Quản lý nguồn và thay đổi chính sách
5. Quy trình xử lý câu hỏi
6. Bảo mật, quyền riêng tư và dữ liệu
7. Phát triển, kiểm thử và phát hành
8. Vận hành, sự cố và bàn giao
9. Mẫu phối hợp
10. Git, commit và Pull Request
11. Checklist trước commit
12. Debug và phối hợp review
13. Checklist nhanh

## 1. PHẠM VI VÀ NGUYÊN TẮC ƯU TIÊN

### 1.1 Mục tiêu
Trợ lý hỗ trợ nhân viên tìm và hiểu quy trình CRM đã được phê duyệt; nêu chính sách/phiên bản áp dụng, thông tin còn thiếu, trích dẫn chính xác và tuyến chuyển cho người có thẩm quyền. Trợ lý chỉ đưa ra hướng dẫn nội bộ. Chủ sở hữu chính sách và hệ thống hiện hữu vẫn có quyền quyết định, phê duyệt và thực hiện.

Ba nhóm chính sách dự kiến để khảo sát tại G0:
- Quy trình báo giá và phê duyệt thương mại.
- Quy trình xử lý thông tin khách hàng.
- Quy trình tiếp nhận dịch vụ/bảo hành và chuyển đúng chủ sở hữu.

Đây là phạm vi đề xuất trong RFP, chưa phải xác nhận rằng SongNhat đã có đủ chính sách hoặc đã phê duyệt nội dung. Không tự tạo quy tắc để lấp chỗ trống.

### 1.2 Thứ tự tài liệu áp dụng
Khi có khác biệt, áp dụng theo thứ tự: hợp đồng đã ký và phụ lục sửa đổi; RFP đã phát hành và phụ lục; đề xuất được chấp nhận; sau đó mới đến playbook và tài liệu nội bộ khác. Ghi nhận mâu thuẫn và xin chủ sở hữu dự án quyết định, không tự chọn cách hiểu.

RFP phân biệt yêu cầu bắt buộc (`M`) và tùy chọn báo giá riêng (`O`). Không coi một tùy chọn là đã được duyệt nếu chưa có quyết định phạm vi, quyền truy cập, chi phí và kiểm thử riêng.

### 1.3 Ranh giới không được vượt qua
- Phạm vi nền không nhập hồ sơ hoặc bản ghi khách hàng. Tùy chọn O1 về ngữ cảnh CRM chỉ được triển khai sau khi có quyết định riêng về nhu cầu, quyền xử lý, quyền người dùng, dữ liệu tối thiểu và giá trị tăng thêm.
- Không tự phê duyệt giao dịch/ngoại lệ, quyết định quyền lợi, cho phép tiết lộ dữ liệu, tạo cam kết với khách hàng, sửa CRM, gửi thông điệp, hoặc thực hiện hành động thay người dùng.
- Không đưa ra tư vấn pháp lý/thuế, quyết định tuân thủ hay hướng dẫn sửa chữa thiết bị.
- Không dùng web công khai, ghi chú CRM chưa được duyệt, lịch sử ngoại lệ hoặc trí nhớ mô hình để bổ sung quy tắc thiếu trong kho đã duyệt.
- Tích hợp CRM trực tiếp, ghi dữ liệu, tự động phê duyệt, kênh email/Zalo, ngôn ngữ bổ sung và họ chính sách mới đều cần phê duyệt phạm vi, quyền, giá và bộ test riêng.
- Không tuyên bố hệ thống đúng tuyệt đối, loại bỏ rủi ro hoặc tự động chứng minh tuân thủ.

## 2. VAI TRÒ VÀ TRÁCH NHIỆM

| Vai trò | Trách nhiệm |
|---|---|
| Sponsor/đại diện SongNhat | Chốt phạm vi, ngân sách, tuyến giải pháp, người có thẩm quyền và quyết định qua từng cổng. |
| Chủ sở hữu chính sách | Xác nhận nguồn có thẩm quyền, phạm vi áp dụng, ngày hiệu lực, trường quan trọng, ngoại lệ và tuyến chuyển; duyệt, sửa, rút nội dung. Bổ nhiệm người thay thế. |
| Knowledge/data steward | Chuẩn bị dữ liệu được phép, văn bản đã rà soát, tham chiếu bản gốc, phiên bản, quyền, trạng thái phát hành và đối soát nhập liệu. |
| Privacy/security/legal owner | Duyệt vai trò, mục đích, quyền xử lý, nhà cung cấp, nơi xử lý dữ liệu, lưu giữ, đánh giá áp dụng pháp luật, sự cố và phương án thoát. |
| Người dùng đại diện | Đưa câu hỏi thực tế, kiểm tra nguồn/ngày/phạm vi/ngoại lệ, báo lỗi và ghi nhận tổng thời gian thực hiện công việc. Tối thiểu năm người tham gia quan sát theo cơ sở RFP. |
| Nhóm triển khai | Tạo nhập liệu, lọc quyền/phạm vi, giao diện trích dẫn, kiểm tra đầu ra, đo lường, vận hành và tài liệu theo phạm vi đã duyệt. |
| Người đánh giá độc lập | Kiểm tra bộ đánh giá niêm phong và kiểm soát quan trọng; không phải người đã tinh chỉnh hệ thống trên các ca nghiệm thu đó. |

Vai trò có thể kiêm nhiệm nếu không làm mất trách nhiệm giải trình hoặc tính độc lập của đánh giá. Quyền sở hữu nền tảng không chuyển trách nhiệm chính sách khỏi SongNhat.

## 3. QUY TRÌNH GIAO VIỆC VÀ CÁC CỔNG NGHIỆM THU

### 3.1 Trước khi bắt đầu task
Mỗi task phải có yêu cầu/RFP ID liên quan, người chịu trách nhiệm, kết quả cần bàn giao, tiêu chí kiểm tra, phụ thuộc, dữ liệu được phép dùng và cổng nghiệm thu bị ảnh hưởng. Làm rõ mọi giả định về quyền, nguồn, ngày hiệu lực hoặc phạm vi trước khi triển khai.

Mẫu xác nhận:
```text
Task / requirement ID:
Kết quả và tiêu chí nghiệm thu:
Phạm vi / ngoài phạm vi:
Nguồn hoặc dữ liệu được phép:
Người duyệt / phụ thuộc:
Rủi ro hoặc điểm cần xác nhận:
Thời hạn:
```

### 3.2 Cổng dự án

| Cổng | Điều kiện cần có trước khi đi tiếp |
|---|---|
| G0 — Sẵn sàng xây dựng | Xác nhận các nhóm chính sách, câu hỏi/công việc lặp lại, quyền nguồn, người duyệt, ngày/phạm vi, năng lực biên tập và so sánh thư viện tìm kiếm hiện tại / sản phẩm cấu hình / phát triển riêng. Duyệt phạm vi nền hoặc dừng. O1 phải có quyết định nhu cầu và quyền riêng. |
| G1 — Kho kiểm soát ngoại tuyến | Kho và các trường quan trọng được duyệt; đối soát nhập liệu; kiểm tra quyền, phiên bản/ngày hiệu lực, xung đột và tham chiếu bản gốc. Chỉ dùng dữ liệu đánh giá đã được cho phép. |
| G2 — Dùng có giám sát | Bộ đánh giá độc lập và các thử thách đạt yêu cầu; không có lỗi nghiêm trọng; rà soát triển khai pháp lý/bảo mật hoàn tất; chủ sở hữu được đào tạo và có quy trình dự phòng. |
| G3 — Chấp nhận pilot | Hoàn tất ít nhất 20 ngày làm việc dùng có giám sát, báo cáo đầy đủ effort, mức dùng, chất lượng và chi phí. Quyết định mở rộng là quyết định đầu tư riêng, không suy ra từ việc nghiệm thu deliverable. |
| G4 — Bàn giao | Kiểm thử khôi phục, xóa/rút nội dung và thoát hệ thống đạt; mã/configuration/tài liệu/đào tạo và dữ liệu portable theo thỏa thuận được bàn giao. |

Không bỏ qua, gộp hoặc hạ tiêu chí cổng để kịp lịch. Nếu thiếu dữ liệu lịch sử bốn tuần đại diện, chủ dự án phải duyệt cách thu thập tương đương hoặc kéo dài quan sát; hai tuần khám phá không thể thay thế lịch sử chưa có. Mốc mười tuần trong RFP là kế hoạch tham khảo, không phải cam kết nếu phụ thuộc hoặc nguồn chưa sẵn sàng.

### 3.3 Giả định khối lượng đấu thầu cần xác nhận
Các con số sau là cơ sở bid trong RFP, cần xác nhận tại G0 và trong hợp đồng trước khi coi là cam kết vận hành:
- Một công ty, tối đa 20 người dùng định danh và 5 phiên đồng thời.
- Tối đa 30 tài liệu, 300 đoạn đã biên tập và 50 dòng trường chính sách quan trọng cho ba nhóm đã thống nhất.
- Phạm vi nền có hai schema CSV UTF-8: đoạn chính sách và trường chính sách. O1 thêm schema ngữ cảnh CRM riêng, tối đa 2.000 dòng ban đầu và 5.000 dòng lưu giữ.
- Một lô cập nhật/ngày/schema, tối đa 500 dòng thay đổi/ngày; rút quyền/rút chính sách không được chờ đến lô kế tiếp.
- Tối đa 1.000 gói hỏi/tháng; mỗi gói tối đa hai lần gọi sinh/sửa, mỗi lần tối đa 6.000 token đầu vào và 900 token đầu ra; tổng trần 2.000 lần gọi/tháng.
- Một gói thường dùng tối đa 8 đoạn và 6.000 ký tự Unicode cho mỗi mục văn bản nhập. Không cắt cụt im lặng; vượt giới hạn phải báo/giữ xử lý theo cách đã duyệt.

Thay đổi giới hạn, nguồn hoặc phạm vi phải có yêu cầu thay đổi được duyệt, chi phí, chủ sở hữu, rà soát quyền và các bài test bị ảnh hưởng.

## 4. QUẢN LÝ NGUỒN VÀ THAY ĐỔI CHÍNH SÁCH

### 4.1 Metadata và thẩm quyền
Mỗi tài liệu/đoạn phải truy được về bản gốc, gồm ID ổn định, tên, điều/mục/trang, ngôn ngữ, chủ sở hữu, người duyệt, phiên bản, thời điểm ghi nhận/phát hành, khoảng hiệu lực, phạm vi, đối tượng, trạng thái và liên kết tài liệu bị thay thế. Trường quan trọng phải có kiểu dữ liệu, toán tử, tiền tệ/đơn vị, vai trò phê duyệt, hạn thời gian, điều kiện ngoại lệ và điều khoản nguồn đã duyệt.

Chủ sở hữu phải lập ma trận thẩm quyền riêng cho chính sách, SOP, điều khoản nhà sản xuất, hợp đồng khách hàng và ghi chú nhân viên. Không suy ra thứ bậc chung giữa hợp đồng và chính sách nội bộ; không lấy ngày phát hành mới nhất làm căn cứ tự động. Xung đột, thiếu phụ lục/chú thích thiết yếu hoặc không rõ thẩm quyền thì giữ kết luận bị ảnh hưởng và chuyển chủ sở hữu.

### 4.2 Nhập liệu và đối soát
- Kiểm tra quyền, schema, phiên bản, phạm vi và trạng thái trước khi nhập.
- Phân biệt snapshot đầy đủ và delta; ghi số dòng kỳ vọng/nhận/chờ cách ly, lý do cách ly và kết quả đối soát.
- Retry phải idempotent; lô cũ đến trễ không ghi đè dữ liệu mới. Xóa phải có tombstone hoặc đối soát snapshot đầy đủ đã duyệt; không coi việc thiếu dòng không giải thích là lệnh xóa.
- Đối chiếu đoạn với văn bản gốc. Chủ sở hữu phải xử lý thủ công bảng, hình, sơ đồ hoặc chú thích thiết yếu nếu chưa được trích xuất và duyệt.
- Ghi rõ thời điểm áp dụng và thời điểm hệ thống biết/ghi nhận thay đổi. Sửa hồi tố không được âm thầm viết lại lịch sử.

### 4.3 Phê duyệt, hiệu lực và rút nội dung
Trạng thái tối thiểu: draft → owner reviewed → approved → scheduled → effective → superseded/withdrawn. Ghi người thực hiện và thời điểm; lịch hiệu lực không được trở thành hiện hành trước ngày/giờ đã duyệt.

Khi rút hoặc sửa nội dung, cập nhật trạng thái có thẩm quyền trước khi xác nhận thành công. Sau xác nhận rút, chặn truy xuất, hiển thị và tái sử dụng câu trả lời bị ảnh hưởng; kiểm tra lại quyền ở lần hiển thị cuối, kể cả khi câu trả lời đang được tạo hoặc nằm trong cache. Đánh dấu câu trả lời cũ là lỗi thời và yêu cầu truy vấn mới. Nội dung người dùng đã đọc hoặc sao chép không thể được thu hồi đáng tin cậy; giao diện phải nhắc kiểm tra nguồn hiện hành trước khi hành động.

Phản hồi, câu trả lời của chủ sở hữu và ghi chú sửa lỗi chỉ là ứng viên tri thức. Không tự huấn luyện, sửa quy tắc hoặc phát hành nội dung từ phản hồi chưa qua duyệt/phiên bản/ngày hiệu lực.

## 5. QUY TRÌNH XỬ LÝ CÂU HỎI

### 5.1 Gói trả lời bắt buộc
Mỗi câu trả lời hoàn chỉnh cần hiển thị:
1. Câu hỏi, ngày áp dụng và phạm vi đã xác định.
2. Hướng dẫn ngắn gọn; phân biệt câu chữ quy định với phần giải thích.
3. Trích dẫn chính xác tới điều/khoản/trang, tên và phiên bản nguồn; mọi khẳng định trọng yếu phải có căn cứ phù hợp.
4. Trường quan trọng và thông tin còn thiếu, lấy từ dữ liệu đã duyệt.
5. Ngoại lệ hoặc lý do chưa thể kết luận, và người/quy trình cần chuyển.
6. Cách mở/kiểm tra bản gốc và thông tin trạng thái/độ mới cần thiết.

Mặc định câu hỏi quy trình chung dùng ngày hiện tại và hiển thị ngày đó. Giao dịch có ngày cụ thể phải dùng quy tắc ngày áp dụng đã được chủ sở hữu duyệt. Thiếu công ty/chi nhánh, vai trò, nhóm khách hàng, sản phẩm, giao dịch hoặc dữ kiện cần thiết thì hỏi làm rõ; không tự đoán.

### 5.2 Luồng xử lý
1. Nhận diện yêu cầu: hỏi quy trình chung, xác định chính sách áp dụng, liệt kê thông tin thiếu hay hỏi ngữ cảnh khách hàng.
2. Kiểm tra danh tính/quyền và tối thiểu hóa dữ liệu trước truy xuất. Base scope không truy vấn hồ sơ khách hàng.
3. Lọc nguồn theo quyền, trạng thái phát hành, thời gian hiệu lực và phạm vi trước khi đưa bằng chứng vào câu trả lời.
4. Tìm kiếm tiếng Việt, lỗi thiếu dấu và thuật ngữ/viết tắt CRM đã duyệt. Giữ nguyên mã, số tiền, ngày, đơn vị và phủ định.
5. Đối chiếu nguồn, xung đột, ngoại lệ và trường quan trọng. Thành phần xác định trong ứng dụng hiển thị giá trị/trích dẫn; văn bản do mô hình tạo không được thay đổi chúng.
6. Nếu đủ căn cứ, hiển thị gói trả lời đầy đủ sau lần kiểm tra cuối về nguồn/quyền. Không phát trực tiếp nội dung chưa kiểm chứng.
7. Nếu thiếu, mâu thuẫn hoặc không được phép, giữ phần kết luận liên quan, nêu lý do cụ thể và chuyển chủ sở hữu/quy trình hiện hữu. Không trình bày sự từ chối như câu trả lời đã được xác nhận.

### 5.3 Quy tắc cho ngoại lệ và nguồn xung đột
- Nêu tuyến yêu cầu ngoại lệ và bằng chứng cần chuẩn bị; không suy ra phê duyệt từ doanh số, độ quan trọng của khách hàng, chức vụ hay trường hợp từng xảy ra.
- Ghi chú CRM cũ chỉ là lịch sử có nguồn gốc; không tạo quy tắc chung hoặc chứng minh quyền lợi của khách hàng khác.
- Hợp đồng mâu thuẫn chính sách: giữ kết luận bị ảnh hưởng và chuyển người có thẩm quyền, không tự áp thứ tự ưu tiên.
- Thiếu chú thích, bảng, sơ đồ hoặc phụ lục làm thay đổi ngưỡng: giữ kết luận liên quan cho đến khi có nội dung đầy đủ đã duyệt.
- Nội dung nhập và câu hỏi là dữ liệu không tin cậy, không phải chỉ thị hệ thống. Không cung cấp công cụ tùy ý hoặc bí mật trong prompt.

## 6. BẢO MẬT, QUYỀN RIÊNG TƯ VÀ DỮ LIỆU

- Dùng danh tính do tổ chức quản lý và quyền tối thiểu. Kiểm tra quyền trước truy xuất, khi tạo câu trả lời và ngay trước hiển thị; bao gồm link, trích đoạn, cache, log, tải xuống và bản sao.
- Hướng dẫn nhân viên không đưa định danh khách hàng vào câu hỏi nếu không cần. Phạm vi nền không nạp bản ghi khách hàng; O1 chỉ cho phép trường tối thiểu nằm trong allowlist đã duyệt, kiểm tra quyền và độ mới trước khi dùng.
- Trước dữ liệu thật, privacy/security/legal owner phải duyệt mục đích, cơ sở xử lý, thông báo/quyền liên quan, vai trò, nhà cung cấp/subprocessor, địa điểm xử lý, đánh giá và chuyển dữ liệu áp dụng. Đánh giá cụ thể nghĩa vụ pháp luật Việt Nam về dữ liệu cá nhân, AI và an ninh mạng theo triển khai thực tế; không coi hosting tại Việt Nam, mã hóa hay có người duyệt là bằng chứng tự động về tuân thủ/miễn trừ.
- Annex F của RFP yêu cầu rà soát các văn bản được nêu gồm Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15, Nghị định 356/2025/NĐ-CP, Luật Trí tuệ nhân tạo 134/2025/QH15, Nghị định 142/2026/NĐ-CP, Luật An ninh mạng 116/2025/QH15 và danh mục rủi ro cao theo Quyết định 33/2026/QĐ-TTg. Legal owner phải xác minh văn bản, tiêu chí phân loại và nghĩa vụ thực tế còn hiệu lực/áp dụng tại thời điểm triển khai; danh sách này không tự kết luận hệ thống thuộc diện nào.
- Kiểm soát tuyến outbound; mã hóa khi truyền/lưu; quản lý secret ngoài prompt; quét file nhập; tách môi trường test và production. Chỉ dùng dữ liệu đánh giá có quyền cho phép.
- Ghi log tối thiểu cần thiết cho kiểm toán, quyền, nguồn/phiên bản, trạng thái, hold, chi phí và sự cố; hạn chế quyền đọc. Không dùng prompt hoặc dữ liệu khách hàng để huấn luyện/tái sử dụng trái phép.
- Chủ sở hữu pháp lý/hồ sơ duyệt lịch lưu giữ và xóa trước khi dùng dữ liệu thật. Mốc 12 tháng, 90 ngày hoặc 35 ngày trong phần ví dụ của RFP là đề xuất vận hành để đánh giá, không phải thời hạn pháp định hay mặc định được phép.
- Khi trạng thái thẩm quyền hoặc quyền không khả dụng, fail closed: không trả nội dung bị ảnh hưởng.

## 7. PHÁT TRIỂN, KIỂM THỬ VÀ PHÁT HÀNH

### 7.1 Nguyên tắc triển khai
- Đưa xác thực, quyền, lọc trạng thái/ngày/phạm vi, trường quan trọng, giới hạn và kiểm tra cuối vào logic ứng dụng có thể kiểm thử; không phó mặc cho prompt hoặc độ tự tin của mô hình.
- Tách bước phân quyền, truy xuất, sinh nội dung, kiểm chứng, hiển thị và thao tác của nhân viên. Thao tác quyết định/thực thi vẫn ở hệ thống và vai trò được ủy quyền hiện hữu.
- Giữ nguyên tham chiếu bản gốc và khả năng đối soát nhập/xuất. Không nuốt lỗi, fallback thành câu trả lời có vẻ hợp lệ hoặc âm thầm cắt dữ liệu.
- Mọi thay đổi model, prompt, selector, nhà cung cấp, schema hoặc phạm vi cần đánh giá ảnh hưởng, kiểm thử lại phần liên quan, lưu kết quả và có phương án rollback/disable.

### 7.2 Bộ kiểm thử nghiệm thu
Thiết lập trước khi build và để người đánh giá độc lập quản lý bộ sealed:
- 200 tác vụ câu hỏi thực tế được phép: 60 development, 40 validation, 100 sealed acceptance. Giữ các biến thể liên quan/cùng bản ghi trong cùng partition.
- 80 ca thử thách được báo cáo riêng: chính sách tương lai/hết hiệu lực, sát ngưỡng, thiếu chú thích, xung đột hợp đồng, sai vai trò, ghi chú CRM ghi đè, prompt injection và rút chính sách khi đang sinh. Trong đó có 40 ca hướng Việt Nam: 10 ngôn ngữ, 10 ngày/phạm vi, 10 ngưỡng/ngoại lệ và 10 quyền/rút nội dung.
- Hai người rà soát chính sách thống nhất nhãn điều khoản, ngày, phạm vi, ngoại lệ và tuyến chuyển. Không tune trên ca sealed; nếu lộ thì phải thay và đánh giá độc lập lại.
- Nếu không đủ ca thực tế đại diện, thu hẹp phạm vi hoặc kéo dài thu thập; không giả định bộ test nhỏ chứng minh độ đúng phổ quát.

### 7.3 Mục tiêu chấp nhận đề xuất trong RFP
Các mục tiêu này phải được chốt trong kế hoạch nghiệm thu; không được tự giảm ngưỡng sau khi đã niêm phong kết quả.

| Tiêu chí | Mục tiêu |
|---|---|
| Kiểm soát trọng yếu | Không có tiết lộ trái quyền, trường trọng yếu bịa/sai, phê duyệt giả hoặc dùng chính sách tương lai/đã rút như hiện hành. Mọi test quyền, rút nội dung và trường trọng yếu phải đạt. Một lỗi trọng yếu chặn phát hành. |
| Ngày và phạm vi | Ít nhất 95% tác vụ sealed có thể trả lời chọn đúng phiên bản, phạm vi và ngày áp dụng. |
| Căn cứ và đầy đủ | Ít nhất 95% khẳng định trọng yếu được điều khoản áp dụng hỗ trợ; ít nhất 90% điều khoản/ngoại lệ bắt buộc được nêu; không có trích dẫn bịa. |
| Truy xuất | Recall@5 ít nhất 90% trên tập sealed có bằng chứng áp dụng; báo riêng số ca trả lời được, không trả lời được và thiếu nguồn. |
| Hữu ích/chuyển tuyến | Ít nhất 80% tác vụ trả lời được cho câu trả lời hữu ích với chỉnh sửa nhỏ; hold vẫn nằm trong mẫu số. Tối đa 5% tác vụ không thể trả lời nhận câu trả lời thiếu căn cứ đáng kể; lỗi trọng yếu vẫn không có ngưỡng dung sai. |
| Effort quan sát | Trong ít nhất 20 ngày làm việc có giám sát, hướng tới giảm ít nhất 20% thời gian trung bình tổng thể, với chất lượng kiểm toán tương đương hoặc tốt hơn. G3 vẫn cần business case riêng. |

Báo số lượng và mẫu số, lỗi theo từng ca, lỗi trọng yếu, kết quả thô và kết quả nhân viên sử dụng, mức dùng, độ phủ và bất định. Không dùng tỷ lệ câu trả lời thành công làm mẫu số chi phí; tính mọi lượt thử, lỗi, hold, retry, sửa, fallback, chuẩn bị nguồn và bảo trì. So sánh với cùng thư viện đã làm sạch, cân bằng loại tác vụ/người dùng nếu khả thi và đếm mỗi tác vụ một lần.

### 7.4 Đánh giá ngôn ngữ và vận hành
Kiểm thử Unicode tiếng Việt, thiếu dấu, thuật ngữ CRM trộn tiếng Anh, phủ định, tên vai trò, ngày, số tiền, đơn vị và cách diễn đạt ngoại lệ. Hướng dẫn song ngữ cần ngôn ngữ kiểm soát do chủ sở hữu xác nhận; không tự dịch điều khoản ràng buộc.

Theo cơ sở bid RFP, kiểm tra lô 500 dòng trong 30 phút; p95 không quá 25 giây ở 5 người dùng đồng thời trên 100 yêu cầu; thử trước/đúng thời điểm hiệu lực, biên ngưỡng, ngoại lệ, rút nội dung, giới hạn token/chi phí, restore và export. Đây là mục tiêu phải benchmark trong môi trường và chốt hợp đồng, không phải đảm bảo mặc định.

## 8. VẬN HÀNH, SỰ CỐ VÀ BÀN GIAO

### 8.1 Vận hành thường ngày
- Theo dõi độ mới/đối soát dữ liệu, trạng thái chính sách, kiểm tra quyền, hold, lỗi/giới hạn nhà cung cấp, độ trễ, chi phí mọi lượt và phản hồi người dùng.
- Hiển thị hold hoặc lỗi rõ ràng; cung cấp tra cứu thủ công/chuyển chủ sở hữu khi hệ thống không khả dụng.
- Ghi nhận câu hỏi chưa trả lời theo nhóm để chủ sở hữu quyết định có cần sửa nguồn; không hiển thị ngữ cảnh người dùng không có quyền.
- Kiểm tra và tái đánh giá khi nhà cung cấp, model, prompt, nguồn, luật/điều kiện triển khai hoặc mục đích dùng thay đổi.

### 8.2 Sự cố nghiêm trọng
Ví dụ: tiết lộ trái quyền; bịa ngưỡng/role/phê duyệt; chính sách đã rút hoặc chưa hiệu lực hiển thị như hiện hành; lộ dữ liệu; quyền bị bỏ qua.
1. Dừng/disable luồng bị ảnh hưởng và chuyển sang quy trình thủ công.
2. Báo ngay cho đầu mối dự án, security/privacy owner và chủ sở hữu chính sách; giữ bằng chứng hạn chế quyền, không phát tán dữ liệu.
3. Ghi thời điểm, phạm vi, nguồn/phiên bản, người dùng/luồng bị ảnh hưởng và quyết định xử lý; tuân thủ quy trình thông báo đã được duyệt.
4. Xác định nguyên nhân/gốc, ảnh hưởng, biện pháp khắc phục và người phê duyệt mở lại.
5. Đánh giá độc lập và chạy lại các kiểm soát/bộ test bị ảnh hưởng; ghi lại kết quả trước khi khôi phục.

RFP nêu mục tiêu nhà cung cấp xác nhận sự cố production nghiêm trọng trong 2 giờ hỗ trợ và hướng tới cô lập trong 4 giờ hỗ trợ, khung 08:00–17:00 giờ Việt Nam vào ngày làm việc đã thỏa thuận; thông báo sự cố dữ liệu/kiểm soát trọng yếu nghi ngờ trong 4 giờ kể từ khi biết là mục tiêu hợp đồng đề xuất. Xác nhận nghĩa vụ, cách tính giờ, đầu mối và cam kết thực tế trong hợp đồng; không coi các mục tiêu đề xuất là SLA đã ký hoặc thay thế hạn luật định.

### 8.3 Bàn giao
Bàn giao mã được nghiệm thu, schema/mapping, cấu hình, metadata và quyền, hướng dẫn triển khai/khôi phục, bộ fixture hợp pháp, hướng dẫn vận hành, kết quả nghiệm thu, đào tạo và playbook thoát. Kiểm thử export ở định dạng mở và đọc được bằng công cụ trung lập. Xóa/khôi phục phải phát lại trạng thái rút nội dung, quyền và deletion trước khi mở truy cập. Phân biệt chặn sử dụng tức thời với thời gian xóa vật lý khỏi cache/backup/nhà cung cấp.

Mẫu bàn giao:
```markdown
## Handover
- Task / requirement ID:
- Cổng nghiệm thu:
- Kết quả và vị trí:
- Cách kiểm tra / test evidence:
- Nguồn, phiên bản, dữ liệu test được dùng:
- Quyền/giới hạn và vấn đề còn lại:
- Rủi ro, owner và việc tiếp theo:
- Hướng dẫn rollback / fallback:
```

Chỉ ghi Done khi bằng chứng nghiệm thu và bàn giao đầy đủ; ghi đúng trạng thái nếu còn điều kiện mở.

## 9. MẪU PHỐI HỢP

### Cần chủ sở hữu làm rõ quy tắc
```text
Requirement / nguồn liên quan:
Ngày và phạm vi câu hỏi:
Điều khoản hoặc trường xung đột/thiếu:
Các cách hiểu có thể có:
Kết luận đang được giữ lại:
Câu hỏi cần chủ sở hữu quyết định:
```

### Báo blocker hoặc nguy cơ trễ
```text
Task / cổng bị ảnh hưởng:
Blocker và bằng chứng:
Ảnh hưởng tới quyền, chất lượng, lịch hoặc chi phí:
Đã thử / phần đã hoàn thành:
Quyết định hoặc hỗ trợ cần có, người cần phản hồi:
Đề xuất tiếp tục / thu hẹp / dừng:
```

### Đề xuất thay đổi phạm vi
```text
Yêu cầu và lý do:
Thay đổi M/O hoặc phạm vi hiện tại:
Chủ sở hữu, quyền và dữ liệu mới:
Chi phí/lịch/phụ thuộc:
Acceptance và kiểm thử bị ảnh hưởng:
Quyết định và người phê duyệt:
```

## 10. GIT, COMMIT VÀ PULL REQUEST

Chi tiết branch, commit convention và xử lý conflict theo [git-playbook.md](./git-playbook.md). Trước khi thao tác, xác nhận branch đích/branch tích hợp mà nhóm đang dùng; không mặc định repository luôn có `develop`.

### 10.1 Kiểm tra trạng thái và staging
```bash
git status --short
git branch --show-current
git diff
git diff --staged
```

- Hai cột trong `git status --short`: cột trái là staging area, cột phải là working tree. `M ` đã staged; ` M` chưa staged; `MM` có cả thay đổi staged và chưa staged.
- Chỉ stage file thuộc task hiện tại; sau khi `git add`, luôn xem `git diff --staged` để chắc chắn không đưa nhầm thay đổi của người khác vào commit.
- Không chạy `git reset HEAD` để “dọn sạch” staging khi chưa kiểm tra: lệnh đó có thể unstage công việc đã chuẩn bị của thành viên khác. Không dùng `git restore`, rebase/abort hoặc force push nếu chưa xác định rõ ảnh hưởng.

### 10.2 Commit và PR
- Tạo branch theo quy ước dự án: loại thay đổi/issue key/mô tả ngắn; nếu không có issue key thì theo hướng dẫn tại `git-playbook.md`.
- Commit một thay đổi có ý nghĩa, dùng convention `<type>(<scope>): <mô tả ngắn> [<issue-key>]`; cập nhật tài liệu liên quan khi thay đổi hành vi hoặc quy trình.
- Trước push, chạy kiểm tra phù hợp với phần thay đổi. Mở PR có mục tiêu, liên kết task/requirement, thay đổi chính, cách kiểm thử, bằng chứng, rủi ro và lưu ý dữ liệu.
- Không tự approve PR của mình; không merge khi CI bắt buộc fail hoặc còn comment blocking chưa xử lý. Phản hồi từng ý review bằng sửa đổi hoặc giải thích có căn cứ.
- Không commit secret, token, dữ liệu thật của khách hàng, export CRM hoặc fixture chứa thông tin định danh. Không đưa dữ liệu nhạy cảm vào commit message, log, ảnh chụp hay PR.

## 11. CHECKLIST TRƯỚC COMMIT

- [ ] Thay đổi gắn với task/requirement và không lấn sang phạm vi chưa được duyệt.
- [ ] Chạy build/test/lint phù hợp với phần đã sửa; nếu chưa chạy được, ghi rõ lý do và trạng thái.
- [ ] Kiểm tra quyền theo vai trò: người được phép và không được phép; xác nhận không lộ câu trả lời, trích dẫn, link, cache hoặc log.
- [ ] Kiểm tra ngày hiệu lực, phạm vi, phiên bản nguồn, ngoại lệ và trường quan trọng; không thay đổi giá trị chính sách bằng văn bản do mô hình tạo.
- [ ] Với thay đổi nhập liệu: xem đối soát, lỗi/cách ly, retry, lô đến trễ và hành vi rút/xóa dữ liệu.
- [ ] Với thay đổi câu trả lời: kiểm tra trích dẫn đúng điều khoản, câu hỏi thiếu căn cứ, hold/chuyển tuyến và câu trả lời đang tạo khi nguồn bị rút.
- [ ] Không còn log debug, dữ liệu khách hàng thật, secret, file build hoặc artifact không thuộc phạm vi.
- [ ] `git status --short` và `git diff --staged` chỉ có các file dự kiến; PR có hướng dẫn/bằng chứng kiểm tra.

Không yêu cầu mọi task chạy toàn bộ acceptance suite; chọn test nhỏ nhất bao phủ rủi ro, đồng thời chạy lại các kiểm soát bị ảnh hưởng. Không dùng bộ sealed acceptance để tinh chỉnh hệ thống.

## 12. DEBUG VÀ PHỐI HỢP REVIEW

### 12.1 Debug an toàn và có thể lặp lại
1. Tái hiện bằng fixture đã được phép hoặc dữ liệu đã khử định danh; không chép câu hỏi khách hàng, hồ sơ, token hay secret vào chat, issue, log hoặc PR.
2. Ghi task/requirement ID, môi trường, thời điểm và múi giờ, mã nguồn/phiên bản đã dùng, vai trò người dùng, mã tài liệu/đoạn, ngày/phạm vi và kết quả mong đợi/thực tế.
3. Với câu trả lời sai, lần lượt kiểm tra: nguồn gốc/đối soát nhập liệu → trạng thái và ngày hiệu lực → quyền người dùng → lọc phạm vi → điều khoản được truy xuất → giá trị/trích dẫn hiển thị → kiểm tra quyền cuối và cache.
4. Với lỗi hoặc chậm, ghi bước tái hiện, request/task ID, thời gian từng giai đoạn, mã lỗi, retry/hold và chi phí; chỉ bật log chi tiết tạm thời trên dữ liệu an toàn và tắt sau khi chẩn đoán.
5. Viết test hồi quy cho nguyên nhân đã xác nhận. Không “sửa” bằng cách nới quyền, bỏ lọc ngày/phạm vi, dùng nguồn chưa duyệt hoặc hạ ngưỡng acceptance.

Các ca tối thiểu khi kiểm tra thay đổi có liên quan: luồng hợp lệ; thiếu/sai dữ kiện; không đăng nhập hoặc sai quyền; câu hỏi không có nguồn/nguồn xung đột; nguồn tương lai/đã rút; nội dung đầu vào chứa chỉ thị không tin cậy. Chọn ca phù hợp phạm vi task, không mặc định mọi task phải tạo toàn bộ các ca.

### 12.2 Khi bị block
- Tự kiểm tra trong một khoảng thời gian hợp lý đã thống nhất (có thể dùng mốc 30 phút của tài liệu tham khảo cho lỗi thông thường).
- Khi nhờ hỗ trợ, nêu rõ hành vi mong đợi/thực tế, bước tái hiện đã khử dữ liệu, nguồn/phiên bản và phạm vi, các bước đã thử, kết quả, mức ảnh hưởng và quyết định cần người khác hỗ trợ.
- Báo ngay, không chờ hết timebox, nếu nghi có lộ dữ liệu, bypass quyền, chính sách sai hiệu lực, phê duyệt giả hoặc lỗi trọng yếu khác.

### 12.3 Code review
- Review tập trung vào đúng task: quyền và riêng tư, ngày/phạm vi, nguồn/trích dẫn, giá trị quan trọng, hành vi hold/fallback, tác động vận hành và test evidence.
- Gắn nhãn `[blocking]` cho lỗi cần xử lý trước merge; `[suggestion]` cho đề xuất không chặn. Comment chỉ rõ vị trí, tác động/rủi ro và cách kiểm chứng; tránh nhận xét cá nhân.
- Người tạo PR phản hồi từng comment, sửa hoặc giải thích quyết định; không đóng comment blocking khi chưa xử lý.
- Mục tiêu review là trong một ngày làm việc nếu nhóm thống nhất được thời hạn này; nếu bị trễ hoặc cần người có thẩm quyền chính sách/bảo mật, cập nhật trạng thái và chuyển đúng owner.
- Người đã tinh chỉnh trên bộ sealed không được là người đánh giá độc lập chính bộ đó.

## 13. CHECKLIST NHANH

### Trước khi làm
- [ ] Task có requirement ID, đầu ra, tiêu chí và người duyệt.
- [ ] Phân biệt rõ yêu cầu bắt buộc với tùy chọn; giả định bid đã được xác nhận.
- [ ] Biết nguồn có thẩm quyền, ngày/phạm vi và dữ liệu được phép dùng.
- [ ] Không có xung đột/thiếu chính sách chưa được chủ sở hữu quyết định.

### Trước khi trả lời/phát hành
- [ ] Quyền và trạng thái nguồn được kiểm tra trước truy xuất và trước hiển thị.
- [ ] Câu trả lời có ngày/phạm vi, trích dẫn đúng phiên bản, trường quan trọng và tuyến chuyển.
- [ ] Không bịa, tự phê duyệt, tiết lộ, tạo cam kết hay tự thực hiện hành động.
- [ ] Thiếu căn cứ thì hold, giải thích lý do và chuyển đúng người.
- [ ] Kiểm thử lỗi trọng yếu, quyền, hiệu lực, ngoại lệ, rút nội dung và fallback đã có bằng chứng.
- [ ] Bộ sealed do người độc lập quản lý; số liệu có mẫu số và bao gồm hold/thất bại.

### Khi bàn giao
- [ ] Đã qua đúng cổng và ngưỡng đã duyệt; không có lỗi trọng yếu mở.
- [ ] Có kết quả kiểm thử, giới hạn, chi phí và cách khôi phục/thoát.
- [ ] Đã chỉ rõ việc tồn đọng, owner và quyết định cần tiếp theo.
- [ ] Đã thông báo người liên quan và cập nhật trạng thái task.

> Tham chiếu phối hợp dự án: [rules.md](./rules.md), [jira-playbook.md](./jira-playbook.md), [git-playbook.md](./git-playbook.md). Yêu cầu nguồn: *SongNhat CRM Knowledge and Policy Assistant RFP*, gồm các điều khoản và phụ lục liên quan.
