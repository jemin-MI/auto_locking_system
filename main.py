import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIntValidator
import sys
import pyautogui
import subprocess
import random
import sys
import time
from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from datetime import datetime, timedelta
import dbus
import dbus.mainloop.glib
from gi.repository import GLib


pyautogui.FAILSAFE= False

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scheduler = BackgroundScheduler()
        self.label = QLabel("APScheduler with PyQt", self)


    def initUI(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Top-right lock icon button
        top_layout = QHBoxLayout()
        top_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.top_lock_button = QPushButton()
        self.top_lock_button.setIcon(QIcon("lock_icon.png"))  # Ensure you have a lock_icon.png
        self.top_lock_button.setIconSize(QSize(30, 30))
        self.top_lock_button.setFixedSize(50, 50)
        self.top_lock_button.setStyleSheet("background-color: transparent; border: none;")
        self.top_lock_button.clicked.connect(self.start_task)
        top_layout.addWidget(self.top_lock_button)
        layout.addLayout(top_layout)

        # Block 1: Timer input with title
        block1_layout = QVBoxLayout()
        title_label = QLabel("Add Your Time for Lock")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        block1_layout.addWidget(title_label)

        timer_layout = QHBoxLayout()
        self.hour_input = QLineEdit()
        self.minute_input = QLineEdit()
        self.second_input = QLineEdit()

        # Setting placeholder texts, input restrictions, and alignment
        self.hour_input.setPlaceholderText("HH")
        self.minute_input.setPlaceholderText("MM")
        self.second_input.setPlaceholderText("SS")

        self.hour_input.setValidator(QIntValidator(0, 99))
        self.minute_input.setValidator(QIntValidator(0, 59))
        self.second_input.setValidator(QIntValidator(0, 59))

        self.hour_input.setAlignment(Qt.AlignCenter)
        self.minute_input.setAlignment(Qt.AlignCenter)
        self.second_input.setAlignment(Qt.AlignCenter)

        # Increased font size of input text
        input_style = "border: 1px solid #ccc; border-radius: 10px; padding: 5px; font-size: 13px;"  # Change font size here
        self.hour_input.setFixedSize(80, 40)
        self.hour_input.setStyleSheet(input_style)
        self.minute_input.setFixedSize(80, 40)
        self.minute_input.setStyleSheet(input_style)
        self.second_input.setFixedSize(80, 40)
        self.second_input.setStyleSheet(input_style)
        

        timer_layout.addWidget(self.hour_input)
        timer_layout.addWidget(QLabel(":"))
        timer_layout.addWidget(self.minute_input)
        timer_layout.addWidget(QLabel(":"))
        timer_layout.addWidget(self.second_input)

        block1_layout.addLayout(timer_layout)
        layout.addLayout(block1_layout)

        # Spacer
        layout.addSpacerItem(QSpacerItem(5, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Block 2: Minute timer and lock button (Removed second lock button)
        block2_layout = QVBoxLayout()
        minute_layout = QHBoxLayout()
        minute_layout.setSpacing(5)  # Reduce spacing between text and input box

        subtitle_label = QLabel("Add Timer for Mouse :")
        subtitle_label.setFont(QFont("Arial", 13, QFont.Bold))
        subtitle_label.setAlignment(Qt.AlignLeft)

        self.only_minute_input = QLineEdit()
        self.only_minute_input.setPlaceholderText("MM")
        self.only_minute_input.setValidator(QIntValidator(0, 59))
        self.only_minute_input.setAlignment(Qt.AlignCenter)
        self.only_minute_input.setFixedSize(80, 40)
        self.only_minute_input.setStyleSheet(input_style)

        minute_layout.addWidget(subtitle_label)
        minute_layout.addWidget(self.only_minute_input)

        block2_layout.addLayout(minute_layout)
        layout.addLayout(block2_layout)

        # Reduce the height of spacer between blocks
        layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Reduced height

        # Block 3: Round start button
        block3_layout = QVBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.start_button.setFixedSize(120, 120)
        self.start_button.setStyleSheet("border-radius: 60px; background-color: #4CAF50; color: white;")
        self.start_button.clicked.connect(self.process_start)
        block3_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        layout.addLayout(block3_layout)

        # Add extra space between start button and warning text
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Block 4: Warning label
        self.warning_label = QLabel("")
        self.warning_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setStyleSheet("color: red;")  # Initially empty, will be updated

        layout.addWidget(self.warning_label)

        # Set main layout
        self.setLayout(layout)
        self.setWindowTitle("Premium Timer Application")
        self.setStyleSheet("""
            background: linear-gradient(to bottom right, #ff7e5f, #feb47b);
        """)
        self.resize(380, 500)  # User-friendly window size

    def process_start(self):
        hour, minute, second = (int(self.hour_input.text() or 0), 
                        int(self.minute_input.text() or 0), 
                        int(self.second_input.text() or 0))
        hover_time = int(self.only_minute_input.text() or 0)

        
        scheduled_time = timedelta(
            hours=int(hour), 
            minutes=int(minute), 
            seconds=int(second) * 60  # Adding hover_time in seconds
)        
        self.start_task(scheduled_time)
        self.wait_for_unlock_after_time(scheduled_time, hover_time)
        
        # Call function to show the warning text
        self.show_warning("Please ensure all inputs are correct!")
    
    
    def wait_for_unlock_after_time(self, scheduled_time, hover_time):
        """Wait for the scheduled time to pass, then check every 5 seconds if the PC is unlocked."""
        
        # Wait until the specified time has passed
        time.sleep(scheduled_time.total_seconds())

        # Start checking every 5 seconds after the time is up
        check_interval = 2  # Check every 5 seconds
        
        def is_screen_locked():
            try:
                result = subprocess.run(['loginctl', 'show', '--property=Locked', '--value'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    locked_status = result.stdout.decode().strip()
                    return locked_status == 'yes'
                else:
                    print("Error checking lock status with loginctl:", result.stderr.decode())
                    return False
            except Exception as e:
                print(f"Error occurred: {e}")
                return False

        # Main loop to check the lock status every 5 seconds
        while True:
            if not is_screen_locked():  # If the PC is unlocked
                print("PC is unlocked!")
                self.mouse_hovering(hover_time)
                break
            time.sleep(check_interval)
            
        
    
    
    
    
    def show_warning(self, message):
        """Function to update the warning message at the bottom of the UI."""
        self.warning_label.setText(message)
    
    def mouse_hovering(self, hover_time):
        hover_time = 1
        loop_count = int( (hover_time*60)//0.5)
        x, y  = pyautogui.size()
        
        for i in range(loop_count):
            x_rand = random.randrange(0, x)
            y_rand = random.randrange(0, y)
            
            if x_rand < x and y_rand < y:
                pyautogui.moveTo(x_rand, y_rand)
                time.sleep(0.5)

        
    def start_task(self, scheduled_time):
        """Schedule a task to run after 20 minutes"""
        run_time = datetime.now() + scheduled_time 
        self.scheduler.add_job(self.on_lock_click, 'date', run_date=run_time)  # Schedule the task
        self.scheduler.start()  # Start the scheduler
        self.label.setText(f"Task scheduled for {run_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    
    def on_lock_click(self):
        subprocess.run(['loginctl', 'lock-session'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())
