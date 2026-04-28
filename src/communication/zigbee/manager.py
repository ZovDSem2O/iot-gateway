# src/communication/zigbee/manager.py
import serial
import time
import json

class ZigBeeManager:
    def __init__(self):
        self.devices = {}  # 存储 ZigBee 设备连接
    
    def add_device(self, device_id, port, baudrate=9600, timeout=1):
        """
        添加 ZigBee 设备
        
        :param device_id: 设备标识
        :param port: 串口端口（如 '/dev/ttyS3'）
        :param baudrate: 波特率，默认 9600
        :param timeout: 超时时间，默认 1 秒
        """
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
        """
        读取 ZigBee 设备数据
        
        :param device_id: 设备标识
        :return: 解析后的数据字典，失败返回 None
        """
        if device_id not in self.devices:
            print(f"ZigBee 设备 {device_id} 未找到")
            return None
        
        ser = self.devices[device_id]
        try:
            # 读取串口数据
            data = ser.readline().decode('utf-8').strip()
            
            if data:
                # 尝试解析 JSON 格式数据
                try:
                    parsed_data = json.loads(data)
                    return parsed_data
                except json.JSONDecodeError:
                    # 如果不是 JSON，直接返回原始数据
                    return {"raw": data}
            return None
        except Exception as e:
            print(f"读取 ZigBee 设备 {device_id} 数据失败: {e}")
            return None
    
    def send_data(self, device_id, data):
        """
        向 ZigBee 设备发送数据
        
        :param device_id: 设备标识
        :param data: 要发送的数据（字符串或字典）
        :return: True 表示成功，False 表示失败
        """
        if device_id not in self.devices:
            print(f"ZigBee 设备 {device_id} 未找到")
            return False
        
        ser = self.devices[device_id]
        try:
            if isinstance(data, dict):
                # 如果是字典，转换为 JSON 字符串
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
        """
        关闭所有 ZigBee 设备连接
        """
        for device_id, ser in self.devices.items():
            try:
                ser.close()
                print(f"ZigBee 设备 {device_id} 连接已关闭")
            except Exception as e:
                print(f"关闭 ZigBee 设备 {device_id} 连接失败: {e}")
        self.devices.clear()