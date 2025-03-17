# main.py
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QImage, QPixmap
import cv2

# Класс для окна с HSV-ползунками
class HsvWindow(QtWidgets.QDialog):
    hsv_changed = pyqtSignal(int, int, int)  # Сигнал для изменения значений HSV

    def __init__(self):
        super().__init__()
        uic.loadUi("hsv_window.ui", self)
        self.setup_sliders()

    def setup_sliders(self):
        self.h_slider.valueChanged.connect(lambda: self.emit_hsv())
        self.s_slider.valueChanged.connect(lambda: self.emit_hsv())
        self.v_slider.valueChanged.connect(lambda: self.emit_hsv())

    def emit_hsv(self):
        h = self.h_slider.value()
        s = self.s_slider.value()
        v = self.v_slider.value()
        self.hsv_changed.emit(h, s, v)

# Основной класс приложения
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        
        # Инициализация переменных
        self.camera_active = False
        self.manual_mode = False
        self.hsv_values = (0, 0, 0)
        
        # Подключение сигналов
        self.btn_mode.clicked.connect(self.toggle_mode)
        self.btn_hsv.clicked.connect(self.show_hsv_window)
        self.btn_start.clicked.connect(self.start_camera)
        self.btn_stop.clicked.connect(self.stop_camera)
        
        # Инициализация кнопок управления
        self.control_buttons = [
            self.btn_forward,
            self.btn_backward,
            self.btn_left,
            self.btn_right
        ]
        self.toggle_control_buttons(False)
        
        # Окно HSV
        self.hsv_window = HsvWindow()
        self.hsv_window.hsv_changed.connect(self.update_hsv)

    def toggle_mode(self):
        self.manual_mode = not self.manual_mode
        mode_text = "Ручной режим" if self.manual_mode else "Авто режим"
        self.btn_mode.setText(mode_text)
        self.toggle_control_buttons(self.manual_mode)

    def toggle_control_buttons(self, visible):
        for btn in self.control_buttons:
            btn.setVisible(visible)

    def show_hsv_window(self):
        self.hsv_window.show()

    def update_hsv(self, h, s, v):
        self.hsv_values = (h, s, v)
        print(f"HSV values updated: {self.hsv_values}")

    def start_camera(self):
        if not self.camera_active:
            self.camera_active = True
            self.cap = cv2.VideoCapture(0)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)

    def stop_camera(self):
        if self.camera_active:
            self.camera_active = False
            self.timer.stop()
            self.cap.release()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Конвертация кадра для отображения
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Обновление изображений
            self.lbl_camera.setPixmap(QPixmap.fromImage(qt_image))
            
            # Здесь можно добавить обработку маски
            # mask = process_frame(frame, self.hsv_values)
            # self.lbl_mask.setPixmap(QPixmap.fromImage(mask))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())