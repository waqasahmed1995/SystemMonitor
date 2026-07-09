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
        self.apply_dark_theme()

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

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
                font-size: 13px;
                font-weight: 500;
                padding: 4px 0px;
            }
            QProgressBar {
                background-color: #313244;
                border: none;
                border-radius: 6px;
                text-align: center;
                color: #cdd6f4;
                height: 22px;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 6px;
            }
            QTextEdit {
                background-color: #181825;
                color: #f38ba8;
                border: 1px solid #313244;
                border-radius: 6px;
                font-family: Consolas, monospace;
                font-size: 12px;
                padding: 6px;
            }
        """)

    def update_metrics(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.cpu_label.setText(f"CPU Usage: {cpu}%")
        self.cpu_bar.setValue(int(cpu))
        self.set_bar_color(self.cpu_bar, cpu)

        self.ram_label.setText(f"RAM Usage: {ram}%")
        self.ram_bar.setValue(int(ram))
        self.set_bar_color(self.ram_bar, ram)

        if cpu > 80.0:
            database.log_alert("CPU", cpu)
            self.log_view.append(f"⚠️ [ALERT] High CPU activity detected: {cpu}%")
        if ram > 85.0:
            database.log_alert("RAM", ram)
            self.log_view.append(f"⚠️ [ALERT] Critical memory consumption: {ram}%")

    def set_bar_color(self, bar, value):
        if value < 60:
            color = "#a6e3a1"  # green
        elif value < 80:
            color = "#f9e2af"  # yellow
        else:
            color = "#f38ba8"  # red
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #313244;
                border: none;
                border-radius: 6px;
                text-align: center;
                color: #1e1e2e;
                height: 22px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitorApp()
    window.show()
    sys.exit(app.exec())