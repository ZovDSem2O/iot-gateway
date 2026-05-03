import sqlite3
import json
import time
from datetime import datetime

class DataStorage:
    def __init__(self, db_path="gateway_data.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type TEXT NOT NULL,
                device_id TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                raw_data TEXT,
                timestamp TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()

    def insert_data(self, device_type, device_id, temperature=None, humidity=None, raw_data=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO sensor_data 
            (device_type, device_id, temperature, humidity, raw_data, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (device_type, device_id, temperature, humidity, str(raw_data), now, now))
        
        conn.commit()
        conn.close()
        
        return True

    def get_latest_data(self, device_type=None, device_id=None, limit=1):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM sensor_data'
        params = []
        
        if device_type:
            query += ' WHERE device_type = ?'
            params.append(device_type)
        if device_id:
            query += ' WHERE device_id = ?'
            params.append(device_id)
        
        query += ' ORDER BY id DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        
        return result

    def get_data_by_time_range(self, start_time, end_time, device_type=None, device_id=None, limit=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM sensor_data WHERE created_at BETWEEN ? AND ?'
        params = [start_time, end_time]
        
        if device_type:
            query += ' AND device_type = ?'
            params.append(device_type)
        if device_id:
            query += ' AND device_id = ?'
            params.append(device_id)
        
        query += ' ORDER BY created_at ASC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        
        return result

    def get_data_count(self, device_type=None, device_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT COUNT(*) FROM sensor_data'
        params = []
        
        if device_type:
            query += ' WHERE device_type = ?'
            params.append(device_type)
        if device_id:
            query += ' WHERE device_id = ?'
            params.append(device_id)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        
        return result[0]

    def get_all_devices(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT device_type, device_id FROM sensor_data')
        result = cursor.fetchall()
        conn.close()
        
        return result