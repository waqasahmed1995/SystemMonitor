import sys
import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QProgressBar, QPushButton, QTextEdit)
from PySide6.QtCore import QTimer, Qt
import database

class SystemMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Industrial System Health Monitor")
        self.resize(450, 400)

        # Initialize Database
        database.init_db()

        # UI Layout Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # CPU Section
        self.cpu_label = QLabel("CPU Usage: 0%")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.main_layout.addWidget(self.cpu_label)
        self.main_layout.addWidget(self.cpu_bar)

        # RAM Section
        self.ram_label = QLabel("RAM Usage: 0%")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.main_layout.addWidget(self.ram_label)
        self.main_layout.addWidget(self.ram_bar)

        # Incident Log Area
        self.log_label = QLabel("Recent Threshold Incidents:")
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.main_layout.addWidget(self.log_label)
        self.main_layout.addWidget(self.log_view)

        # Background Interval Timer (Simulating real-time polling)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(2000)  # Updates every 2 seconds

    def update_metrics(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.cpu_label.setText(f"CPU Usage: {cpu}%")
        self.cpu_bar.setValue(int(cpu))

        self.ram_label.setText(f"RAM Usage: {ram}%")
        self.ram_bar.setValue(int(ram))

        if cpu > 80.0:
            database.log_alert("CPU", cpu)
            self.log_view.append(f"⚠️ [ALERT] High CPU activity detected: {cpu}%")
        if ram > 85.0:
            database.log_alert("RAM", ram)
            self.log_view.append(f"⚠️ [ALERT] Critical memory consumption: {ram}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitorApp()
    window.show()
    sys.exit(app.exec())