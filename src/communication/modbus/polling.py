import threading
import time
from .modbus import ModbusManager

class ModbusPoller:
    """Modbus设备轮询类"""
    
    def __init__(self):
        """初始化轮询器"""
        self.modbus_manager = ModbusManager()
        self.devices = {}  # 存储设备信息
        self.running = False
        self.thread = None
        
    def add_device(self, device_id, device_type, **params):
        """
        添加设备
        :param device_id: 设备ID
        :param device_type: 设备类型（rtu/tcp）
        :param params: 设备参数
        """
        self.devices[device_id] = {
            'type': device_type,
            'params': params,
            'data': {}
        }
        print(f"添加设备成功: {device_id}")
        
    def start_polling(self, interval=1):
        """
        开始轮询
        :param interval: 轮询间隔（秒）
        """
        self.running = True
        self.thread = threading.Thread(target=self._polling_loop, args=(interval,))
        self.thread.daemon = True
        self.thread.start()
        print("开始轮询设备")
        
    def stop_polling(self):
        """停止轮询"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("停止轮询设备")
        
    def _polling_loop(self, interval):
        """轮询循环"""
        while self.running:
            for device_id, device_info in self.devices.items():
                try:
                    # 确保设备已连接
                    if not self._ensure_connected(device_id, device_info):
                        continue
                    
                    # 读取设备数据
                    data = self._read_device_data(device_id, device_info)
                    if data:
                        self.devices[device_id]['data'] = data
                        print(f"设备 {device_id} 数据: {data}")
                        
                except Exception as e:
                    print(f"轮询设备 {device_id} 异常: {e}")
                    
            time.sleep(interval)
            
    def _ensure_connected(self, device_id, device_info):
        """
        确保设备已连接
        :param device_id: 设备ID
        :param device_info: 设备信息
        :return: 是否连接成功
        """
        if device_info['type'] == 'rtu':
            # 检查是否已创建客户端
            if device_id not in self.modbus_manager.rtu_clients:
                params = device_info['params']
                self.modbus_manager.create_rtu_client(
                    device_id,
                    params.get('port'),
                    params.get('baudrate', 9600),
                    params.get('timeout', 1)
                )
            # 连接设备
            return self.modbus_manager.connect(device_id)
            
        elif device_info['type'] == 'tcp':
            # 检查是否已创建客户端
            if device_id not in self.modbus_manager.tcp_clients:
                params = device_info['params']
                self.modbus_manager.create_tcp_client(
                    device_id,
                    params.get('host'),
                    params.get('port', 502),
                    params.get('timeout', 1)
                )
            # 连接设备
            return self.modbus_manager.connect(device_id)
            
        return False
        
    def _read_device_data(self, device_id, device_info):
        """
        读取设备数据
        :param device_id: 设备ID
        :param device_info: 设备信息
        :return: 读取的数据
        """
        params = device_info['params']
        slave_id = params.get('slave_id', 1)
        address = params.get('address', 0)
        count = params.get('count', 2)
        
        # 读取保持寄存器
        data = self.modbus_manager.read_holding_registers(
            device_id,
            slave_id,
            address,
            count
        )
        
        if data:
            return {
                'timestamp': time.time(),
                'values': data
            }
        return None
        
    def get_device_data(self, device_id):
        """
        获取设备数据
        :param device_id: 设备ID
        :return: 设备数据
        """
        if device_id in self.devices:
            return self.devices[device_id]['data']
        return None

# 测试代码
if __name__ == "__main__":
    poller = ModbusPoller()
    
    # 添加RTU设备
    poller.add_device(
        'sensor1',
        'rtu',
        port='/dev/ttyS4',
        baudrate=9600,
        slave_id=1,
        address=0,
        count=2
    )
    
    # 添加TCP设备（可选）
    # poller.add_device(
    #     'sensor2',
    #     'tcp',
    #     host='192.168.1.100',
    #     port=502,
    #     slave_id=1,
    #     address=0,
    #     count=2
    # )
    
    # 开始轮询
    poller.start_polling(interval=2)
    
    # 运行10秒
    time.sleep(10)
    
    # 停止轮询
    poller.stop_polling()