import unittest
import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sensors.temperature_humidity import TemperatureHumiditySensor

class TestTemperatureHumiditySensor(unittest.TestCase):
    """测试温湿度传感器"""
    
    def test_init(self):
        """测试初始化"""
        sensor = TemperatureHumiditySensor('test', '/dev/ttyS4')
        self.assertIsNotNone(sensor)
        
    def test_read_data(self):
        """测试读取数据"""
        sensor = TemperatureHumiditySensor('test', '/dev/ttyS4')
        if sensor.connect():
            data = sensor.read_data()
            print(f"测试数据: {data}")
            sensor.close()
        else:
            print("连接失败，跳过测试")

if __name__ == "__main__":
    unittest.main()