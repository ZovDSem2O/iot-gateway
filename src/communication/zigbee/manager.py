import serial
import time
import json

class ZigBeeManager:
    def __init__(self):
        self.devices = {}

    def add_device(self, device_id, port, baudrate=9600, timeout=1):
        try:
            ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
            self.devices[device_id] = ser
            print(f"ZigBee 设备 {device_id} 连接成功，端口: {port}")
            return True
        except Exception as e:
            print(f"ZigBee 设备 {device_id} 连接失败: {e}")
            return False

    def read_data(self, device_id):
        if device_id not in self.devices:
            print(f"ZigBee 设备 {device_id} 未找到")
            return None

        ser = self.devices[device_id]
        try:
            data = ser.readline().decode('utf-8').strip()

            if data:
                try:
                    parsed_data = json.loads(data)
                    return parsed_data
                except json.JSONDecodeError:
                    return {"raw": data}
            return None
        except Exception as e:
            print(f"读取 ZigBee 设备 {device_id} 数据失败: {e}")
            return None

    def send_data(self, device_id, data):
        if device_id not in self.devices:
            print(f"ZigBee 设备 {device_id} 未找到")
            return False

        ser = self.devices[device_id]
        try:
            if isinstance(data, dict):
                data_str = json.dumps(data) + '\n'
            else:
                data_str = str(data) + '\n'

            ser.write(data_str.encode('utf-8'))
            print(f"向 ZigBee 设备 {device_id} 发送数据: {data_str}")
            return True
        except Exception as e:
            print(f"向 ZigBee 设备 {device_id} 发送数据失败: {e}")
            return False

    def close(self):
        for device_id, ser in self.devices.items():
            try:
                ser.close()
                print(f"ZigBee 设备 {device_id} 连接已关闭")
            except Exception as e:
                print(f"关闭 ZigBee 设备 {device_id} 连接失败: {e}")
        self.devices.clear()