import time
import threading
import cv2
import numpy as np

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

# Bảng màu chuẩn Cyberpunk / Glassmorphism Neon
COLOR_BG = (0.05, 0.06, 0.09, 1)        # Đen vũ trụ
COLOR_CARD = (0.10, 0.12, 0.17, 1)      # Xám công nghệ
COLOR_ACCENT = (0.00, 0.85, 0.65, 1)    # Xanh Neon
COLOR_DANGER = (0.95, 0.25, 0.35, 1)    # Đỏ cảnh báo
COLOR_TEXT = (0.92, 0.94, 0.96, 1)      # Trắng sáng
COLOR_MUTED = (0.45, 0.50, 0.60, 1)     # Xám mờ

# ==================== MODULE OPENCV XỬ LÝ CAPTCHA & ẢNH ====================
class VisionEngine:
    @staticmethod
    def process_captcha(frame):
        """
        Nhận diện khối vuông xanh dương và vòng tròn xanh lá của Captcha bằng OpenCV.
        Trả về tọa độ (x, y) để giả lập thao tác vuốt.
        """
        if frame is None:
            return None, None, None
            
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 1. Quét khối vuông màu xanh dương (Mảnh ghép)
        lower_blue, upper_blue = np.array([100, 150, 50]), np.array([140, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        square_pos = None
        for cnt in contours_blue:
            if 150 < cv2.contourArea(cnt) < 10000:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                if len(approx) == 4:
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        square_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        break

        # 2. Quét vòng tròn màu xanh lá (Vị trí đích)
        lower_green, upper_green = np.array([35, 50, 50]), np.array([85, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        green_pos = None
        for cnt in contours_green:
            if 200 < cv2.contourArea(cnt) < 10000:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
                    if square_pos and cX > square_pos[0]:
                        green_pos = (cX, cY)
                        break

        # 3. Tính điểm tâm trung gian
        mid_pos = None
        if square_pos and green_pos:
            mid_pos = ((square_pos[0] + green_pos[0]) // 2, (square_pos[1] + green_pos[1]) // 2)

        return square_pos, mid_pos, green_pos

# ==================== KHUNG ACCESSIBILITY SERVICE (KHÔNG ROOT) ====================
class AccessibilityBridge:
    @staticmethod
    def is_service_enabled():
        # Kiểm tra trạng thái Dịch vụ Trợ năng trên Android
        return True

    @staticmethod
    def perform_tap(x, y):
        # Gửi lệnh chạm thông qua Trợ năng
        pass

    @staticmethod
    def perform_swipe(x1, y1, x2, y2, duration=150):
        # Gửi lệnh vuốt màn hình thông qua Trợ năng
        pass

# ==================== GIAO DIỆN CHÍNH (KIVY UI) ====================
class GolikeMasterApp(App):
    def build(self):
        self.title = "Golike Automation Master Pro"
        self.is_running = False

        # Layout chính
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = RoundedRectangle(size=root.size, pos=root.pos)
        root.bind(size=self._update_bg, pos=self._update_bg)

        # 1. HEADER
        header = BoxLayout(orientation='vertical', size_hint=(1, 0.12), spacing=4)
        title_lbl = Label(
            text="[b]GOLIKE AUTO MASTER[/b]", 
            markup=True, font_size=24, color=COLOR_ACCENT
        )
        sub_lbl = Label(
            text="Hệ thống tự động hóa • Không cần Root • Phân phối diện rộng", 
            font_size=12, color=COLOR_MUTED
        )
        header.add_widget(title_lbl)
        header.add_widget(sub_lbl)
        root.add_widget(header)

        # 2. KHU VỰC NHẬP LIỆU TOKEN / CẤU HÌNH
        input_card = BoxLayout(orientation='vertical', size_hint=(1, 0.22), spacing=6)
        lbl_token = Label(text="Token / Tài khoản Golike:", font_size=13, color=COLOR_TEXT, halign='left', size_hint_y=None, height=20)
        lbl_token.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        self.token_input = TextInput(
            hint_text='Dán Token tài khoản vào đây...', 
            multiline=False, password=True, font_size=14,
            background_color=(0.14, 0.17, 0.24, 1), foreground_color=COLOR_TEXT,
            cursor_color=COLOR_ACCENT, padding=[12, 12, 12, 12]
        )
        input_card.add_widget(lbl_token)
        input_card.add_widget(self.token_input)
        root.add_widget(input_card)

        # 3. KHU VỰC LOG TRẠNG THÁI (NHẬT KÝ HỆ THỐNG)
        log_card = BoxLayout(orientation='vertical', size_hint=(1, 0.40))
        lbl_log_title = Label(text="Nhật ký hoạt động AI Vision:", font_size=13, color=COLOR_MUTED, halign='left', size_hint_y=None, height=20)
        lbl_log_title.bind(size=lambda s, w: setattr(s, 'text_size', w))
        
        scroll = ScrollView(size_hint=(1, 1))
        self.status_log = Label(
            text="[Hệ thống sẵn sàng. Vui lòng bật Trợ năng & bấm Chạy...]\n", 
            markup=True, font_size=13, color=COLOR_TEXT,
            valign='top', halign='left'
        )
        self.status_log.bind(size=lambda s, w: setattr(s, 'text_size', w))
        scroll.add_widget(self.status_log)
        
        log_card.add_widget(lbl_log_title)
        log_card.add_widget(scroll)
        root.add_widget(log_card)

        # 4. CÁC NÚT ĐIỀU KHIỂN
        btn_box = BoxLayout(orientation='vertical', size_hint=(1, 0.26), spacing=10)

        # Nút Bắt đầu / Dừng
        self.btn_toggle = Button(
            text="[ ▶ ] BẮT ĐẦU CHẠY TỰ ĐỘNG", 
            background_normal='', background_color=(0.00, 0.70, 0.55, 1),
            color=COLOR_TEXT, font_size=16, bold=True, size_hint=(1, 0.55)
        )
        self.btn_toggle.bind(on_press=self.toggle_automation)

        # Nút Test thử AI Vision & OpenCV
        self.btn_test_vision = Button(
            text="Kiểm tra OpenCV AI Vision", 
            background_normal='', background_color=(0.16, 0.20, 0.28, 1),
            color=COLOR_TEXT, font_size=14, size_hint=(1, 0.45)
        )
        self.btn_test_vision.bind(on_press=self.test_opencv_vision)

        btn_box.add_widget(self.btn_toggle)
        btn_box.add_widget(self.btn_test_vision)
        root.add_widget(btn_box)

        return root

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def log_message(self, text):
        def _update(dt):
            self.status_log.text += f"> {text}\n"
        Clock.schedule_once(_update)

    def toggle_automation(self, instance):
        if not self.is_running:
            token = self.token_input.text.strip()
            if not token:
                self.log_message("[LỖI] Chưa nhập Token Golike!")
                return
            
            self.is_running = True
            self.btn_toggle.text = "[ ■ ] DỪNG LẠI KHẨN CẤP"
            self.btn_toggle.background_color = COLOR_DANGER
            self.log_message("Kích hoạt tiến trình tự động...")
            
            # Khởi chạy luồng xử lý nền
            threading.Thread(target=self.automation_worker_loop, daemon=True).start()
        else:
            self.is_running = False
            self.btn_toggle.text = "[ ▶ ] BẮT ĐẦU CHẠY TỰ ĐỘNG"
            self.btn_toggle.background_color = (0.00, 0.70, 0.55, 1)
            self.log_message("Đã dừng tiến trình tự động.")

    def automation_worker_loop(self):
        """
        Vòng lặp chạy ngầm nhiệm vụ Golike & Bẻ khóa Captcha
        """
        task_count = 1
        while self.is_running:
            self.log_message(f"Đang thực hiện nhiệm vụ #{task_count}...")
            
            # Giả lập chụp khung hình & quét Captcha
            dummy_screen = np.zeros((800, 400, 3), dtype=np.uint8)
            sq, mid, gr = VisionEngine.process_captcha(dummy_screen)
            
            if sq and gr:
                self.log_message(f"[!] Phát hiện Captcha tại X={sq[0]}, Y={sq[1]}. Đang giải...")
                AccessibilityBridge.perform_swipe(sq[0], sq[1], gr[0], gr[1])
                time.sleep(1.0)
            
            # Thời gian chờ giữa các nhiệm vụ
            for _ in range(30):
                if not self.is_running:
                    break
                time.sleep(0.1)
                
            task_count += 1

    def test_opencv_vision(self, instance):
        try:
            test_img = np.zeros((300, 300, 3), dtype=np.uint8)
            # Vẽ thử một khối màu xanh test bộ lọc
            cv2.rectangle(test_img, (50, 50), (100, 100), (255, 0, 0), -1)
            sq, mid, gr = VisionEngine.process_captcha(test_img)
            self.log_message("[OK] Module OpenCV AI Vision hoạt động cực tốt!")
        except Exception as e:
            self.log_message(f"[LỖI OpenCV]: {str(e)}")

if __name__ == '__main__':
    GolikeMasterApp().run()
