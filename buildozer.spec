[app]

# (str) Tên ứng dụng hiển thị trên màn hình điện thoại
title = Golike Pro

# (str) Tên gói định danh duy nhất của app
package.name = golikepro

# (str) Tên miền của gói
package.domain = org.golike

# (list) Các định dạng file nguồn được phép đưa vào app
source.include_exts = py,png,jpg,kv,atlas

# (list) Thư mục chứa mã nguồn (mặc định là thư mục hiện tại)
source.include_dir = .

# (list) Danh sách các thư viện Python bắt buộc phải đóng gói chung vào APK
requirements = python3,kivy,opencv-python,numpy

# (str) Phiên bản ứng dụng
version = 1.0.1

# (list) Các quyền truy cập hệ thống (Permissions)
# Bắt buộc có INTERNET để gọi API Golike, CAMERA/STORAGE để OpenCV xử lý ảnh/captcha
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Hướng hiển thị ứng dụng (portrait = dọc màn hình)
orientation = portrait

# (bool) Chỉ định ứng dụng chạy ở chế độ toàn màn hình
fullscreen = 0

# (str) Định dạng icon của ứng dụng (có thể thay thế bằng file icon.png của ông sau)
#icon.filename = %(source.dir)s/icon.png

[buildozer]

# (int) Mức độ chi tiết của log khi build (0 = chỉ lỗi, 1 = thông tin, 2 = debug chi tiết)
log_level = 2

# (int) Hiển thị cảnh báo khi chạy build bằng tài khoản root (0 = tắt, 1 = bật)
warn_on_root = 1

# (str) Thư mục lưu trữ mã nguồn biên dịch (để mặc định)
#build_dir = .buildozer

# (str) Thư mục chứa file APK sau khi build xong (.bin)
bin_dir = ./bin

[android]

# (int) API Android tối thiểu mà app hỗ trợ (API 21 tương đương Android 5.0 trở lên)
android.min_api = 21

# (int) API Android mục tiêu để biên dịch
android.target_api = 31

# (str) Kiến trúc CPU hỗ trợ (để arm64-v8a hoặc armeabi-v7a để chạy tốt trên đa số máy)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Tự động chấp nhận các điều khoản bản quyền SDK của Google khi build
android.accept_sdk_license = True