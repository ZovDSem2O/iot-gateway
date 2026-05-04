import sqlite3
from datetime import datetime


class AlertManager:
    def __init__(self, db_path="gateway_data.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type TEXT NOT NULL,
                device_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                alert_message TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                is_resolved INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_alert(self, device_type, device_id, alert_type, alert_message, temperature=None, humidity=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO alerts 
            (device_type, device_id, alert_type, alert_message, temperature, humidity, is_resolved, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        ''', (device_type, device_id, alert_type, alert_message, temperature, humidity, now))
        
        conn.commit()
        conn.close()
    
    def get_unresolved_alerts(self, device_type=None, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if device_type:
            cursor.execute('SELECT * FROM alerts WHERE is_resolved = 0 AND device_type = ? ORDER BY id DESC LIMIT ?', (device_type, limit))
        else:
            cursor.execute('SELECT * FROM alerts WHERE is_resolved = 0 ORDER BY id DESC LIMIT ?', (limit,))
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def resolve_alert(self, alert_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE alerts SET is_resolved = 1 WHERE id = ?', (alert_id,))
        
        conn.commit()
        conn.close()