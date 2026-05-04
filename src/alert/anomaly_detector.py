class AnomalyDetector:
    def __init__(self):
        self.rules = {
            'temperature': {'min': 0, 'max': 80, 'unit': '°C'},
            'humidity': {'min': 20, 'max': 90, 'unit': '%'},
        }
    
    def check(self, temperature=None, humidity=None):
        anomalies = []
        
        if temperature is not None:
            if temperature < self.rules['temperature']['min']:
                anomalies.append(f"温度过低: {temperature}°C (正常: {self.rules['temperature']['min']}-{self.rules['temperature']['max']}°C)")
            elif temperature > self.rules['temperature']['max']:
                anomalies.append(f"温度过高: {temperature}°C (正常: {self.rules['temperature']['min']}-{self.rules['temperature']['max']}°C)")
        
        if humidity is not None:
            if humidity < self.rules['humidity']['min']:
                anomalies.append(f"湿度过低: {humidity}% (正常: {self.rules['humidity']['min']}-{self.rules['humidity']['max']}%)")
            elif humidity > self.rules['humidity']['max']:
                anomalies.append(f"湿度过高: {humidity}% (正常: {self.rules['humidity']['min']}-{self.rules['humidity']['max']}%)")
        
        return anomalies