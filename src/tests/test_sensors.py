import unittest
from communication.sensors.temperature_humidity import TemperatureHumiditySensor

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

if __name__ == '__main__':
    unittest.main()