# Gợi ý người quen bằng MapReduce

Bài chủ đề 2: gợi ý tối đa 2 người chưa kết bạn, xếp theo số bạn chung giảm dần và tên tăng dần khi hòa điểm. Chạy bằng Python 3.10+; không cần cài thư viện ngoài.

## Chạy trên Windows, Linux hoặc macOS

Mở terminal trong thư mục dự án:

```text
python run_local.py
python -m unittest discover -s tests -v
python run_local.py --input data/sample.jsonl --output results --top-k 2
```

Một số máy dùng `python3` thay cho `python`.

## Đầu vào

UTF-8 JSON Lines: mỗi dòng là một người và danh sách bạn.

```json
{"user":"Alice","friends":["Bob","Carol"]}
```

Tên phân biệt chữ hoa/thường, sắp theo thứ tự chuỗi Python (Unicode), không dùng quy tắc từ điển tiếng Việt. Trim khoảng trắng đầu/cuối. Gộp bản ghi trùng người; loại bạn trùng và tự kết bạn; bổ sung chiều ngược cho quan hệ một chiều. Người chỉ xuất hiện trong danh sách bạn cũng được tạo. Các sửa đổi ghi vào `results/audit.json`. Dòng sai cấu trúc khiến chương trình dừng với số dòng, không âm thầm bỏ qua.

## Hai lượt MapReduce

1. Tiền xử lý tạo danh sách kề đối xứng.
2. Mapper 1 phát khóa JSON `["PAIR", A, B]`, A < B. Value `["DIRECT"]` đánh dấu bạn trực tiếp; `["MUTUAL", X]` xác định bạn chung X. Khóa `["USER", X]` giữ cả người không có ứng viên.
3. Shuffle 1 sắp theo chuỗi khóa chính xác, gom cùng khóa.
4. Reducer 1 bỏ cặp trực tiếp; đếm bạn chung khác nhau, xuất điểm và danh sách bạn chung.
5. Mapper 2 phát mỗi cặp theo cả hai chiều, khóa là tên người nhận gợi ý.
6. Shuffle 2 gom theo người nhận.
7. Reducer 2 chọn Top K, xuất cả người có danh sách rỗng.

Các script trong `src/` dùng stdin/stdout với giao thức `key<TAB>value`. Reducer yêu cầu đầu vào đã sắp xếp theo key. Không áp dụng Combiner cộng số đơn giản vì value chứa dấu quan hệ và danh tính bạn chung.

## Kết quả mẫu

| Người | Top 2 |
|---|---|
| Alice | Dan (1), Eve (1) |
| Bob | Eve (2), Frank (1) |
| Carol | Dan (2) |
| Dan | Carol (2), Alice (1) |
| Eve | Bob (2), Alice (1) |
| Frank | Bob (1), Eve (1) |

Frank và Eve có bạn chung Dan; bảng mẫu trong đề thiếu gợi ý Eve cho Frank.

## Minh chứng

`results/` chứa input chuẩn hóa, báo cáo sửa dữ liệu, đầu ra hai Mapper, hai bảng Shuffle, điểm cặp và kết quả cuối JSONL. `docs/manual_verification.md` giải thích các điểm bằng tay. Bộ kiểm thử kiểm tra mẫu, người cô lập, trùng bạn/tự kết bạn, quan hệ một chiều, mạng đã kết bạn hết, hòa điểm/Top 2, input sai và 12 đồ thị ngẫu nhiên đối chiếu thuật toán tập hợp độc lập.

## Giới hạn và mở rộng

Nút có d bạn sinh d(d-1)/2 cặp. Tổng số bản ghi ứng viên là tổng đại lượng này trên mọi nút. Nút nhiều bạn gây tăng chi phí và dữ liệu lệch giữa các khóa. Local runner và tiền xử lý lưu dữ liệu trong RAM, chỉ là mô phỏng, không chứng minh khả năng chạy dữ liệu lớn. Reducer 1 lưu tập bạn chung cho một cặp; Reducer 2 chỉ giữ K gợi ý.

Có thể chạy hai lượt với Hadoop Streaming, dùng normalized.jsonl làm đầu vào lượt 1, đầu ra lượt 1 làm đầu vào lượt 2; phân phối cả common.py cùng script qua `-files`. Tiền xử lý dữ liệu rất lớn cần thiết kế một job chuẩn hóa riêng. Chạy Hadoop thật cần môi trường Hadoop và kiểm thử thực tế, bài hiện tại đã kiểm thử local.

Biến thể đề xuất: Jaccard = số bạn chung / số người trong hợp hai danh sách bạn. Cần bổ sung bậc của hai nút để tính mẫu số; biến thể này chưa được cài đặt. Dùng dữ liệu giả cho demo; với dữ liệu thật, cần kiểm soát quyền truy cập và tránh tiết lộ danh tính bạn chung trái với quyền riêng tư.

## Đưa lên GitHub

Tạo repository trống rồi chạy trong thư mục này (thay URL bằng repository của bạn):

```bash
git init
git add .
git commit -m "Add MapReduce friend recommendation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/friend-recommendation-mapreduce.git
git push -u origin main
```

Bổ sung slide 6–10 trang, báo cáo PDF 3–5 trang và bảng phân công trước khi nộp. Bộ mã này chưa bao gồm các tài liệu đó.
