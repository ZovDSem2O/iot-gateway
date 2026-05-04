from flask import Flask, render_template, jsonify
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import DataStorage
from alert.alert_manager import AlertManager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sensors')
def api_sensors():
    storage = DataStorage()
    data = storage.get_latest_data(limit=10)
    result = []
    for row in data:
        result.append({
            'id': row[0],
            'device_type': row[1],
            'device_id': row[2],
            'temperature': row[3],
            'humidity': row[4],
            'timestamp': row[6],
            'created_at': row[7]
        })
    return jsonify(result)

@app.route('/api/alerts')
def api_alerts():
    manager = AlertManager()
    alerts = manager.get_unresolved_alerts(limit=10)
    result = []
    for row in alerts:
        result.append({
            'id': row[0],
            'device_type': row[1],
            'device_id': row[2],
            'alert_type': row[3],
            'alert_message': row[4],
            'temperature': row[5],
            'humidity': row[6],
            'created_at': row[8]
        })
    return jsonify(result)

@app.route('/sensors')
def sensors():
    return render_template('sensors.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)