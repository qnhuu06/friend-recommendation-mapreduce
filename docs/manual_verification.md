# Đối soát bằng tay

## Ví dụ Map

Bob có Alice, Carol, Dan: phát MUTUAL Bob cho (Alice,Carol), (Alice,Dan), (Carol,Dan), cùng dấu DIRECT cho (Alice,Bob), (Bob,Carol), (Bob,Dan).

Dan có Bob, Eve, Frank: phát MUTUAL Dan cho (Bob,Eve), (Bob,Frank), (Eve,Frank), cùng dấu DIRECT cho (Bob,Dan), (Dan,Eve), (Dan,Frank).

## Cặp được giữ sau Reduce 1

| Cặp | Bạn chung | Điểm |
|---|---|---|
| Alice, Dan | Bob | 1 |
| Alice, Eve | Carol | 1 |
| Bob, Eve | Carol, Dan | 2 |
| Bob, Frank | Dan | 1 |
| Carol, Dan | Bob, Eve | 2 |
| Eve, Frank | Dan | 1 |

Các cặp ứng viên (Alice,Carol) qua Bob và (Alice,Bob) qua Carol có DIRECT nên bị loại. Không sinh ứng viên không có bạn chung. Một cặp có thể tồn tại ở cả hai danh sách gợi ý, nhưng chỉ có một khóa cặp vô hướng tại lượt 1.

## Đối soát lượt 2

Dan có Carol (2), Alice (1), lấy cả hai. Eve có Bob (2), Alice (1), Frank (1): lấy Bob và Alice vì Alice đứng trước Frank khi hòa điểm. Frank có Bob (1), Eve (1): lấy cả hai. Carol chỉ có Dan (2), vì vậy xuất một gợi ý.
