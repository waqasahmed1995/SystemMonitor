import sys
import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QProgressBar, QPushButton, QTextEdit,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import QTimer, Qt
import database

class SystemMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Industrial System Health Monitor")
        self.resize(500, 450)
        self.apply_dark_theme()

        database.init_db()

        # Tab widget replaces the old single central_widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.live_tab = QWidget()
        self.history_tab = QWidget()

        self.tabs.addTab(self.live_tab, "Live Monitor")
        self.tabs.addTab(self.history_tab, "Alert History")

        self.build_live_tab()
        self.build_history_tab()

        # Refresh history whenever user clicks that tab
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(2000)

    def build_live_tab(self):
        layout = QVBoxLayout(self.live_tab)

        self.cpu_label = QLabel("CPU Usage: 0%")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)

        self.ram_label = QLabel("RAM Usage: 0%")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)

        self.log_label = QLabel("Recent Threshold Incidents:")
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_label)
        layout.addWidget(self.log_view)

    def build_history_tab(self):
        layout = QVBoxLayout(self.history_tab)

        self.refresh_button = QPushButton("Refresh History")
        self.refresh_button.clicked.connect(self.load_history)
        layout.addWidget(self.refresh_button)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "Timestamp", "Metric", "Value", "Status"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.history_table)

        self.load_history()

    def load_history(self):
        rows = database.get_all_alerts()
        self.history_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.history_table.setItem(row_index, col_index, item)

    def on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Alert History":
            self.load_history()

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
            color = "#a6e3a1"
        elif value < 80:
            color = "#f9e2af"
        else:
            color = "#f38ba8"
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
            QTabWidget::pane {
                border: 1px solid #313244;
                background-color: #1e1e2e;
            }
            QTabBar::tab {
                background-color: #313244;
                color: #cdd6f4;
                padding: 8px 16px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #74c7ec;
            }
            QTableWidget {
                background-color: #181825;
                color: #cdd6f4;
                gridline-color: #313244;
                border: 1px solid #313244;
            }
            QHeaderView::section {
                background-color: #313244;
                color: #cdd6f4;
                padding: 4px;
                border: none;
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitorApp()
    window.show()
    sys.exit(app.exec())