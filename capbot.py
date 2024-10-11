# 캡처된 이미지도 봇한테 쏨
# 봇 토큰과 챗 아이디 입력 받도록 수정
import sys
import os
import time
import traceback
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QMessageBox, QSlider, QHBoxLayout, QLineEdit, QGroupBox, QFormLayout
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen
from PIL import Image, ImageChops
import asyncio
from telegram import Bot
from telegram.error import TelegramError
import pyautogui

class ScreenCaptureWidget(QWidget):
    capture_completed = pyqtSignal(tuple)
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:black;")
        self.setWindowOpacity(0.3)
        self.setGeometry(QApplication.primaryScreen().geometry())
        
        self.begin = None
        self.end = None
        self.show()

    def paintEvent(self, event):
        if self.begin and self.end:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            painter.drawRect(min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y()),
                             abs(self.end.x() - self.begin.x()), abs(self.end.y() - self.begin.y()))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.capture_completed.emit(self.getRect())
        self.close()

    def getRect(self):
        return (
            min(self.begin.x(), self.end.x()),
            min(self.begin.y(), self.end.y()),
            max(self.begin.x(), self.end.x()),
            max(self.begin.y(), self.end.y())
        )

class ScreenMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = 'screen_monitor_config.json'
        self.save_path = ""
        self.monitor_area = None
        self.check_delay = 1
        self.last_image = None
        self.last_check_time = 0
        self.last_save_time = 0
        self.save_cooldown = 0.5  # 0.5초 쿨다운
        self.monitoring = False
        self.bot = None
        self.chat_id = None
        self.start_time = None
        self.loop = asyncio.new_event_loop()  # 새로운 이벤트 루프 생성
        asyncio.set_event_loop(self.loop)  # 루프 설정
        self.load_config()
        self.initUI()
        self.show_guide()

    def initUI(self):
        self.setWindowTitle('변화감지 캡처봇 v0.0024')
        self.setGeometry(100, 100, 400, 400)  # Increased width to accommodate new fields

        layout = QVBoxLayout()

        # Telegram Settings Group
        telegram_group = QGroupBox("Telegram 설정")
        telegram_layout = QFormLayout()

        self.bot_token_input = QLineEdit(self)
        self.bot_token_input.setEchoMode(QLineEdit.Password)
        self.bot_token_input.setPlaceholderText("봇 토큰을 입력하세요")
        telegram_layout.addRow(QLabel("봇 토큰:"), self.bot_token_input)

        self.chat_id_input = QLineEdit(self)
        self.chat_id_input.setPlaceholderText("챗 ID를 입력하세요")
        telegram_layout.addRow(QLabel("챗 ID:"), self.chat_id_input)

        self.save_telegram_btn = QPushButton('저장', self)
        self.save_telegram_btn.clicked.connect(self.save_telegram_settings)
        telegram_layout.addRow(self.save_telegram_btn)

        self.delete_telegram_btn = QPushButton('삭제', self)
        self.delete_telegram_btn.clicked.connect(self.delete_telegram_settings)
        telegram_layout.addRow(self.delete_telegram_btn)

        telegram_group.setLayout(telegram_layout)
        layout.addWidget(telegram_group)

        # Existing UI Elements
        self.path_label = QLabel('저장 경로: 선택되지 않음', self)
        layout.addWidget(self.path_label)

        self.area_label = QLabel('감지 영역: 선택되지 않음', self)
        layout.addWidget(self.area_label)

        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel('체크 딜레이 (초):'))
        self.delay_slider = QSlider(Qt.Horizontal)
        self.delay_slider.setMinimum(1)
        self.delay_slider.setMaximum(10)
        self.delay_slider.setValue(self.check_delay)
        self.delay_slider.setTickPosition(QSlider.TicksBelow)
        self.delay_slider.setTickInterval(1)
        self.delay_slider.valueChanged.connect(self.update_delay)
        delay_layout.addWidget(self.delay_slider)
        self.delay_label = QLabel(str(self.check_delay))
        delay_layout.addWidget(self.delay_label)
        layout.addLayout(delay_layout)

        self.select_path_btn = QPushButton('저장 경로 선택', self)
        self.select_path_btn.clicked.connect(self.select_save_path)
        layout.addWidget(self.select_path_btn)

        self.select_area_btn = QPushButton('감지 영역 선택', self)
        self.select_area_btn.clicked.connect(self.select_area)
        layout.addWidget(self.select_area_btn)

        self.start_stop_btn = QPushButton('모니터링 시작', self)
        self.start_stop_btn.clicked.connect(self.toggle_monitoring)
        layout.addWidget(self.start_stop_btn)

        self.status_label = QLabel('대기 중...', self)
        layout.addWidget(self.status_label)

        made_by_label = QLabel('Made by 충', self)
        made_by_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(made_by_label)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_screen)

        self.telegram_timer = QTimer(self)
        self.telegram_timer.timeout.connect(self.send_telegram_status)
        self.telegram_timer.start(3600000)  # 1시간(3600000 밀리초)마다 실행

        self.update_ui_from_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.save_path = config.get('save_path', '')
            self.monitor_area = tuple(config.get('monitor_area', (0, 0, 0, 0)))
            self.check_delay = config.get('check_delay', 1)
            self.bot_token = config.get('bot_token', '')
            self.chat_id = config.get('chat_id', None)
            if self.bot_token and self.chat_id:
                self.bot = Bot(token=self.bot_token)
        except FileNotFoundError:
            pass  # 파일이 없으면 기본값 사용

    def save_config(self):
        config = {
            'save_path': self.save_path,
            'monitor_area': self.monitor_area,
            'check_delay': self.check_delay,
            'bot_token': getattr(self, 'bot_token', ''),
            'chat_id': getattr(self, 'chat_id', None)
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def update_ui_from_config(self):
        self.path_label.setText(f'저장 경로: {self.save_path if self.save_path else "선택되지 않음"}')
        self.area_label.setText(f'감지 영역: {self.monitor_area if self.monitor_area else "선택되지 않음"}')
        self.delay_slider.setValue(self.check_delay)
        self.delay_label.setText(str(self.check_delay))
        self.bot_token_input.setText(self.bot_token if hasattr(self, 'bot_token') else '')
        self.chat_id_input.setText(str(self.chat_id) if self.chat_id else '')
        self.check_start_conditions()

    def show_guide(self):
        guide_text = (
            "사용법 안내\n\n"
            "1. Telegram 설정에서 봇 토큰과 챗 ID를 입력하고 저장하세요.\n"
            "2. 스크린샷이 저장될 폴더를 지정하세요.\n"
            "3. 변화를 감지할 영역을 드래그 하세요.\n"
            "4. 체크딜레이 타임을 설정하세요.\n"
            "5. 모니터링 시작 버튼을 누르면 동작합니다.\n\n\n\n"
            "* 텔레그램 토큰 및 챗 id입력시 텔레크램으로 안내를 받을 수 있습니다.\n"
            "* 자세한건 구글링 해 보면 관련 자료 많이 나오니까 이런건 직접 스스로... ㄷㄷㄷㄷ"
        )
        QMessageBox.information(self, "사용법 안내", guide_text)

    def select_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, '저장 경로 선택')
        if self.save_path:
            self.path_label.setText(f'저장 경로: {self.save_path}')
            self.check_start_conditions()
            self.save_config()

    def select_area(self):
        try:
            self.hide()
            self.capture_widget = ScreenCaptureWidget()
            self.capture_widget.capture_completed.connect(self.onCaptureFinished)
        except Exception as e:
            self.show()
            self.showErrorMessage("영역 선택 오류", f"영역 선택 중 오류가 발생했습니다: {str(e)}")

    def onCaptureFinished(self, rect):
        try:
            self.monitor_area = rect
            self.area_label.setText(f'감지 영역: {self.monitor_area}')
            self.show()
            self.check_start_conditions()
            self.save_config()
        except Exception as e:
            self.showErrorMessage("영역 선택 완료 오류", f"영역 선택 완료 처리 중 오류가 발생했습니다: {str(e)}")

    def update_delay(self, value):
        self.check_delay = value
        self.delay_label.setText(str(value))
        self.save_config()

    def check_start_conditions(self):
        if self.save_path and self.monitor_area and self.bot_token and self.chat_id:
            self.start_stop_btn.setEnabled(True)
        else:
            self.start_stop_btn.setEnabled(False)

    def toggle_monitoring(self):
        try:
            if not self.monitoring:
                if not self.bot_token or not self.chat_id:
                    self.showErrorMessage("Telegram 설정 오류", "Telegram 봇 토큰과 챗 ID를 먼저 설정하세요.")
                    return
                self.monitoring = True
                self.start_stop_btn.setText('모니터링 중지')
                self.timer.start(100)  # 0.1초마다 체크
                self.status_label.setText('모니터링 중...')
                self.last_check_time = time.time()
                self.start_time = time.time()
                self.send_start_message()
            else:
                self.monitoring = False
                self.start_stop_btn.setText('모니터링 시작')
                self.timer.stop()
                self.status_label.setText('모니터링 중지됨')
                self.send_telegram_message("모니터링이 중지되었습니다.")
        except Exception as e:
            self.showErrorMessage("모니터링 토글 오류", f"모니터링 상태 변경 중 오류가 발생했습니다: {str(e)}")

    def check_screen(self):
        try:
            current_time = time.time()
            if current_time - self.last_check_time < self.check_delay:
                return

            self.last_check_time = current_time
            current_image = self.grab_screen(self.monitor_area)
            
            if current_image is not None and self.last_image is not None:
                diff = ImageChops.difference(current_image, self.last_image)
                if diff.getbbox():
                    if current_time - self.last_save_time >= self.save_cooldown:
                        filepath = self.save_screenshot(current_image)
                        self.send_telegram_screenshot_alert(filepath)
                        self.last_save_time = current_time
            
            self.last_image = current_image
        except Exception as e:
            self.showErrorMessage("화면 체크 오류", f"화면 체크 중 오류가 발생했습니다: {str(e)}")
            self.toggle_monitoring()

    def grab_screen(self, bbox):
        try:
            left, top, right, bottom = bbox
            width = right - left
            height = bottom - top
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            if screenshot.size != (width, height):
                screenshot = screenshot.crop((0, 0, width, height))
            
            return screenshot
        except Exception as e:  
            self.showErrorMessage("스크린샷 캡처 오류", f"스크린샷 캡처 중 오류가 발생했습니다: {str(e)}")
            return None

    def save_screenshot(self, image):
        try:
            timestamp = int(time.time())
            filename = f'screenshot_{timestamp}.png'
            filepath = os.path.join(self.save_path, filename)
            image.save(filepath)
            self.status_label.setText(f'스크린샷 저장됨: {filepath}')
            return filepath
        except Exception as e:
            self.showErrorMessage("스크린샷 저장 오류", f"스크린샷 저장 중 오류가 발생했습니다: {str(e)}")
            return None

    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def send_telegram_message(self, message):
        try:
            if not self.bot:
                raise TelegramError("봇이 초기화되지 않았습니다.")
            # Instead of using the event loop directly, use asyncio.run() to handle the coroutine
            self.loop.run_until_complete(self._send_message_async(message))
        except TelegramError as e:
            self.showErrorMessage("Telegram 오류", f"메시지 전송 중 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            self.showErrorMessage("예상치 못한 오류", f"오류가 발생했습니다: {str(e)}")
    
    async def _send_message_async(self, message):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except TelegramError as e:
            self.showErrorMessage("Telegram 오류", f"메시지 전송 중 오류가 발생했습니다: {str(e)}")

    def send_telegram_screenshot_alert(self, filepath):
        if filepath:
            message = f"화면 변화가 감지되어 스크린샷이 생성되었습니다.\n파일: {os.path.basename(filepath)}"
            self.send_telegram_message(message)
            try:
                # Use asyncio.run() to handle sending the photo asynchronously
                self.loop.run_until_complete(self._send_photo_async(filepath))
            except TelegramError as e:
                self.showErrorMessage("Telegram 오류", f"스크린샷 전송 중 오류가 발생했습니다: {str(e)}")
            except Exception as e:
                self.showErrorMessage("예상치 못한 오류", f"오류가 발생했습니다: {str(e)}")
    
    async def _send_photo_async(self, filepath):
        try:
            with open(filepath, 'rb') as photo:
                await self.bot.send_photo(chat_id=self.chat_id, photo=photo)
        except TelegramError as e:
            self.showErrorMessage("Telegram 오류", f"스크린샷 전송 중 오류가 발생했습니다: {str(e)}")

    def save_telegram_settings(self):
        bot_token = self.bot_token_input.text().strip()
        chat_id = self.chat_id_input.text().strip()

        if not bot_token or not chat_id:
            self.showErrorMessage("입력 오류", "봇 토큰과 챗 ID를 모두 입력해야 합니다.")
            return

        # Validate chat_id is an integer
        try:
            chat_id = int(chat_id)
        except ValueError:
            self.showErrorMessage("입력 오류", "챗 ID는 숫자여야 합니다.")
            return

        # Initialize bot to verify token
        try:
            bot = Bot(token=bot_token)
            # Send a test message to verify bot and chat_id
            self.loop.run_until_complete(bot.send_message(chat_id=chat_id, text="Telegram 설정이 성공적으로 저장되었습니다."))
        except TelegramError as e:
            self.showErrorMessage("Telegram 오류", f"Telegram 설정이 유효하지 않습니다: {str(e)}")
            return
        except Exception as e:
            self.showErrorMessage("예상치 못한 오류", f"오류가 발생했습니다: {str(e)}")
            return

        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = bot
        self.save_config()
        self.check_start_conditions()
        QMessageBox.information(self, "성공", "Telegram 설정이 저장되었습니다.")

    def delete_telegram_settings(self):
        reply = QMessageBox.question(
            self, '삭제 확인',
            "Telegram 설정을 정말 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.bot_token = ''
            self.chat_id = None
            self.bot = None
            self.bot_token_input.clear()
            self.chat_id_input.clear()
            self.save_config()
            self.check_start_conditions()
            QMessageBox.information(self, "삭제 완료", "Telegram 설정이 삭제되었습니다.")

    def send_start_message(self):  # Added this method
        ip_address = self.get_ip_address()
        message = f"화면 모니터링 프로그램이 시작되었습니다.\nIP 주소: {ip_address}"
        self.send_telegram_message(message)

    def get_ip_address(self):  # Added this method
        try:
            response = requests.get('https://api.ipify.org')
            return response.text
        except Exception:
            return "IP 주소를 가져올 수 없습니다."

    def send_telegram_status(self):  # Added this method
        if self.monitoring and self.start_time:
            hours = int((time.time() - self.start_time) / 3600)
            self.send_telegram_message(f"{hours}시간째 정상 동작 중입니다.")

    def closeEvent(self, event):
        if self.monitoring:
            self.toggle_monitoring()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    try:
        ex = ScreenMonitor()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {str(e)}")
        print("상세 오류 정보:")
        print(traceback.format_exc())
        QMessageBox.critical(None, "치명적 오류", f"프로그램 실행 중 치명적인 오류가 발생했습니다:\n{str(e)}")
        sys.exit(1)
