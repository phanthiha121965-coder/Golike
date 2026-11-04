[app]
# Tên ứng dụng hiển thị trên điện thoại
title = Golike Master Pro
# Tên gói ứng dụng (không chứa ký tự đặc biệt)
package.name = golikemaster
# Domain của ông
package.domain = org.dung
# Thư mục chứa mã nguồn (dấu . nghĩa là thư mục hiện tại)
source.dir = .
# Các loại file sẽ được đóng gói vào APK
source.include_exts = py,png,jpg,kv,atlas
# Phiên bản
version = 1.0
# Các thư viện Python cần thiết (Dùng opencv-python-headless để không bị lỗi GUI trên Android)
requirements = python3,kivy,numpy,opencv-python-headless
# Hướng màn hình dọc
orientation = portrait
# Full màn hình
fullscreen = 0
# Cấp quyền cho ứng dụng
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, BIND_ACCESSIBILITY_SERVICE
# Kiến trúc chip Android hỗ trợ
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
# Mức độ chi tiết của log (2 = info)
log_level = 2
warn_on_root = 1
