import sys
import time
import random
import subprocess
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize,  QTimer

from apscheduler.schedulers.background import BackgroundScheduler
import pyautogui

pyautogui.FAILSAFE = False


class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scheduler = BackgroundScheduler()
        self.label = QLabel(self)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Top-right lock icon button
        top_layout = QHBoxLayout()
        top_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.top_lock_button = QPushButton()
        self.top_lock_button.setIcon(QIcon("lock_icon.png"))  # Add a valid icon path
        self.top_lock_button.setIconSize(QSize(30, 30))
        self.top_lock_button.setFixedSize(50, 50)
        self.top_lock_button.setStyleSheet("background-color: transparent; border: none;")
        self.top_lock_button.clicked.connect(self.on_lock_click)
        top_layout.addWidget(self.top_lock_button)
        layout.addLayout(top_layout)

        # Timer input block
        layout.addLayout(self.create_timer_input_block())

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Minute input block
        layout.addLayout(self.create_minute_input_block())

        # Add spacer between the minute input block and the start button
        layout.addSpacerItem(QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Start button
        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.start_button.setFixedSize(240, 80)
        self.start_button.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #388E3C;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Darker shade on hover */
                border-color: #2c6f2f;
            }
            QPushButton:pressed {
                background-color: #388E3C;  /* Darkest shade when pressed */
                border-color: #1c5120;
            }
        """)
        self.start_button.clicked.connect(self.process_start)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)



        # Warning label
        self.warning_label = QLabel("")
        self.warning_label.setFont(QFont("Arial", 10))
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setStyleSheet("color: red;")
        layout.addWidget(self.warning_label)

        # Info label
        self.info_label = QLabel("")
        self.info_label.setFont(QFont("Arial", 10))
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: blue;")
        layout.addWidget(self.info_label)

        # Set window properties
        self.setLayout(layout)
        self.setWindowTitle("Auto Locking")
        self.setStyleSheet("background: linear-gradient(to bottom right, #ff7e5f, #feb47b);")
        self.resize(380, 500)


    def create_timer_input_block(self):
        block = QVBoxLayout()
        
        # Title label
        title_label = QLabel("Add Your Time for Lock")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        block.addWidget(title_label)

        # Add spacer between title and timer input fields
        block.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Timer input fields layout
        timer_layout = QHBoxLayout()
        input_style = "border: 1px solid #ccc; border-radius: 10px; padding: 5px; font-size: 13px;"

        self.hour_input = self.create_input("HH", 80, 40, QIntValidator(0, 99), input_style)
        self.minute_input = self.create_input("MM", 80, 40, QIntValidator(0, 59), input_style)
        self.second_input = self.create_input("SS", 80, 40, QIntValidator(0, 59), input_style)

        timer_layout.addWidget(self.hour_input)
        timer_layout.addWidget(QLabel(":"))
        timer_layout.addWidget(self.minute_input)
        timer_layout.addWidget(QLabel(":"))
        timer_layout.addWidget(self.second_input)
        block.addLayout(timer_layout)

        return block


    def create_minute_input_block(self):
        block = QHBoxLayout()
        subtitle_label = QLabel("Add Timer for Mouse:")
        subtitle_label.setFont(QFont("Arial", 13, QFont.Bold))
        subtitle_label.setAlignment(Qt.AlignLeft)

        input_style = "border: 1px solid #ccc; border-radius: 10px; padding: 5px; font-size: 13px;"
        self.only_minute_input = self.create_input("MM", 80, 40, QIntValidator(0, 59), input_style)

        block.addWidget(subtitle_label)
        block.addWidget(self.only_minute_input)
        return block

    def create_input(self, placeholder, width, height, validator, style):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setValidator(validator)
        input_field.setAlignment(Qt.AlignCenter)
        input_field.setFixedSize(width, height)
        input_field.setStyleSheet(style)
        return input_field

    def highlight_input_border(self):
    # Set border to red for 4 seconds
        def reset_border():
            self.hour_input.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 5px; font-size: 13px;")
            self.minute_input.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 5px; font-size: 13px;")
            self.second_input.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 5px; font-size: 13px;")
        
        # Set border to red
        self.hour_input.setStyleSheet("border: 0.5px solid #a11e15; border-radius: 10px; padding: 5px; font-size: 13px;")
        self.minute_input.setStyleSheet("border: 0.5px solid #a11e15; border-radius: 10px; padding: 5px; font-size: 13px;")
        self.second_input.setStyleSheet("border: 0.5px solid #a11e15; border-radius: 10px; padding: 5px; font-size: 13px;")
        
        # Set a timer to reset the border after 4 seconds
        QTimer.singleShot(4000, reset_border)
    
    def process_start(self):
        try:
            hour = int(self.hour_input.text() or 0)
            minute = int(self.minute_input.text() or 0)
            second = int(self.second_input.text() or 0)
            hover_time = int(self.only_minute_input.text() or 0)
            
            if hour == 0 and minute == 0 and second == 0 and hover_time == 0:
                self.highlight_input_border()
                self.show_log(f"Please Select Time First", "Red")
                
            else:
                
                scheduled_time = timedelta(hours=hour, minutes=minute, seconds=second)
                # Format remaining time as HH:MM:SS
                hours, remainder = divmod(scheduled_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                self.start_task(scheduled_time)
                self.show_log(f"Time remaining to lock PC {formatted_time}", "Green")
                time.sleep(scheduled_time.total_seconds())
                self.wait_for_unlock_after_time(hover_time)
                

        except Exception as e:
            print("fff")
            self.show_log(f"Error: {str(e)}", "Red")

    def wait_for_unlock_after_time(self, hover_time):

        check_interval = 5  # Check every 5 seconds

        def is_screen_locked():
            try:
                result = subprocess.run(
                    ['loginctl', 'show-session', 'self', '--property=LockedHint'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if result.returncode == 0:
                    return "yes" in result.stdout.decode().strip()
                else:
                    return False
            except Exception as e:
                self.show_log(f"Error checking lock status: {str(e)}", "Red")
                return False

        while True:
            if not is_screen_locked():
                
                if hover_time:
                    self.show_log("Screen Unlocked. Starting Mouse Hovering...", "Green")
                    self.mouse_hovering(hover_time)
                break
            time.sleep(check_interval)

    def show_log(self, message, type_, timer_detail=None, time_left=None):
        """
        Display messages on the UI with different styles based on the type.
        :param message: The main message to display.
        :param type_: Type of message: 'Red', 'Green', 'Blue'.
        :param timer_detail: Optional details about the timer.
        :param time_left: Optional time left for the process.
        """
        self.clear_message()
        styled_message = f"<b>{message}</b>"
        print("hitt arived", message)
        if timer_detail:
            styled_message += f"<br><span style='font-size: 11px;'>Timer Details: {timer_detail}</span>"
        if time_left:
            styled_message += f"<br><span style='font-size: 11px;'>Time Left: {time_left}</span>"

        if type_ == 'Red':
            self.warning_label.setStyleSheet("color: red; font-weight: bold;")
            self.warning_label.setText(styled_message)
        elif type_ == 'Green':
            self.info_label.setStyleSheet("color: green; font-weight: bold;")
            self.info_label.setText(styled_message)
        elif type_ == 'Blue':
            self.info_label.setStyleSheet("color: blue; font-weight: bold;")
            self.info_label.setText(styled_message)
        
        QTimer.singleShot(5000, self.clear_message)
        
    def clear_message(self):
        """
        Clear the message from the labels after the set timeout.
        """
        self.warning_label.clear()
        self.info_label.clear()

    def mouse_hovering(self, hover_time):
        x, y = pyautogui.size()
        for _ in range(int((hover_time * 60) / 0.5)):
            print("Hovering...")
            pyautogui.moveTo(random.randint(0, x), random.randint(0, y))
            time.sleep(0.5)

    def start_task(self, scheduled_time):
        run_time = datetime.now() + scheduled_time
        self.scheduler.add_job(self.on_lock_click, 'date', run_date=run_time)
        self.scheduler.start()

    def on_lock_click(self):
        try:
            subprocess.run(['loginctl', 'lock-session'], check=True)
        except Exception as e:
            self.show_log(f"Lock failed: {str(e)}", "Red")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())
