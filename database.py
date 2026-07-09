import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("system_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            metric_type TEXT,
            value REAL,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_alert(metric_type, value, status="WARNING"):
    conn = sqlite3.connect("system_logs.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO alerts (timestamp, metric_type, value, status) VALUES (?, ?, ?, ?)",
        (timestamp, metric_type, value, status)
    )
    conn.commit()
    conn.close()

def get_all_alerts():
    conn = sqlite3.connect("system_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, metric_type, value, status FROM alerts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_all_alerts():
    conn = sqlite3.connect("system_logs.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()