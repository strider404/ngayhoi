# Quy tắc kỷ luật cho Agent

## 1. Vùng mã nguồn được phép sửa
- Chỉ được phép tạo mới hoặc chỉnh sửa mã nguồn trong thư mục `backend/` (ví dụ: `backend/main.py`, tạo thêm route mới hoặc test mới do chính Agent viết như `backend/tests/test_con_cho.py`).

## 2. Vùng cấm chạm (Tuyệt đối không sửa đổi)
- `.github/` (bao gồm toàn bộ thư mục `.github/workflows/` và các cấu hình CI).
- `backend/tests/test_gioi_han.py` (bộ test chuẩn mực của giảng viên / con người).
- Không tự ý sửa `spec.md` nếu không có yêu cầu rõ ràng.
- Không sửa `ui/` trừ khi có chỉ định giao việc làm frontend.

## 3. Quy định kích thước PR (Pull Request)
- Kích thước mỗi Pull Request (PR) phải nhỏ và tập trung, **không vượt quá 200 dòng diff** (tổng số dòng `+` và `-`).
- Làm đúng một tính năng hoặc một phạm vi công việc nhỏ được giao; dừng lại ngay khi toàn bộ test liên quan chuyển sang màu xanh (passed).
- Luôn viết test trước hoặc đi kèm với tính năng mới.

