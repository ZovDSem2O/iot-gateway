from _typeshed import Self
from pymodbus.client import ModbusSerialClient, ModbusTcpClient
from pymodbus.exceptions import ModbusException
from .modbus import ModbusManager
from communication.modbus import ModbusManager
import time

class ModbusManager:
    """Modbus通信管理类"""

    def __init__(self) -> None:
        """初始化Modebus管理器"""
        self.rtu_clients = {}  # 存储RTU客户端
        self.tcp_clients = {}  # 存储TCP客户端

    def create_rtu_client(self, client_id, port, baudrate=9600, timeout=1):
        """
        创建Modbus RTU客户端
        :param client_id: 客户端ID
        :param port: 串口设备路径
        :param baudrate: 波特率
        :param timeout: 超时时间
        :return: 客户端对象
        """
        try:
            client = ModbusSerialClient(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                parity='N',
                stopbits=1,
                bytesize=8
            )
            self.rtu_clients[client_id] = client
            print(f"创建Modbus RTU客户端成功: {client_id}")
            return client
        except Exception as e:
            print(f"创建Modbus RTU客户端失败: {e}")
            return None
    
    def create_tcp_client(self, client_id: str, host: str, port: int = 502, timeout: float = 1.0):
        """
        创建Modbus TCP客户端
        :param client_id: 客户端ID
        :param host: 主机地址
        :param port: 端口号
        :param timeout: 超时时间
        :return: 客户端对象
        """
        try:
            client = ModbusTcpClient(
                host=host,
                port=port,
                timeout=timeout
            )
            self.tcp_clients[client_id] = client
            print(f"TCP客户端 {client_id} 创建成功")
            return client
        except ModbusException as e:
            print(f"创建TCP客户端 {client_id} 失败: {e}")
            return None

    def connect(self, client_id):
        """
        连接Modbus设备
        :param client_id: 客户端ID
        :return: 是否连接成功
        """
        if client_id in self.rtu_clients:
            client = self.rtu_clients[client_id]
        elif client_id in self.tcp_clients:
            client = self.tcp_clients[client_id]
        else:
            print(f"客户端不存在: {client_id}")
            return False
            
        try:
            if not client.is_socket_open():
                client.connect()
            print(f"连接Modbus设备成功: {client_id}")
            return True
        except Exception as e:
            print(f"连接Modbus设备失败: {e}")
            return False

    def read_coils(self, client_id, slave_id, address, count):
        """
        读取线圈（功能码01）
        :param client_id: 客户端ID
        :param slave_id: 从站地址
        :param address: 寄存器地址
        :param count: 读取数量
        :return: 读取结果
        """
        if client_id in self.rtu_clients:
            client = self.rtu_clients[client_id]
        elif client_id in self.tcp_clients:
            client = self.tcp_clients[client_id]
        else:
            print(f"客户端不存在: {client_id}")
            return None
            
        try:
            result = client.read_coils(address, count, slave_id)
            if result.isError():
                print(f"读取线圈失败: {result}")
                return None
            return result.bits
        except Exception as e:
            print(f"读取线圈异常: {e}")
            return None
        
    def read_holding_registers(self, client_id, slave_id, address, count):
        """
        读取保持寄存器（功能码03）
        :param client_id: 客户端ID
        :param slave_id: 从站地址
        :param address: 寄存器地址
        :param count: 读取数量
        :return: 读取结果
        """
        if client_id in self.rtu_clients:
            client = self.rtu_clients[client_id]
        elif client_id in self.tcp_clients:
            client = self.tcp_clients[client_id]
        else:
            print(f"客户端不存在: {client_id}")
            return None
            
        try:
            result = client.read_holding_registers(address, count, slave_id)
            if result.isError():
                print(f"读取保持寄存器失败: {result}")
                return None
            return result.registers
        except Exception as e:
            print(f"读取保持寄存器异常: {e}")
            return None
        
    def write_coil(self, client_id, slave_id, address, value):
        """
        写单个线圈（功能码05）
        :param client_id: 客户端ID
        :param slave_id: 从站地址
        :param address: 寄存器地址
        :param value: 写入值（True/False）
        :return: 是否写入成功
        """
        if client_id in self.rtu_clients:
            client = self.rtu_clients[client_id]
        elif client_id in self.tcp_clients:
            client = self.tcp_clients[client_id]
        else:
            print(f"客户端不存在: {client_id}")
            return False
            
        try:
            result = client.write_coil(address, value, slave_id)
            if result.isError():
                print(f"写线圈失败: {result}")
                return False
            return True
        except Exception as e:
            print(f"写线圈异常: {e}")
            return False
        
    def write_register(self, client_id, slave_id, address, value):
        """
        写单个寄存器（功能码06）
        :param client_id: 客户端ID
        :param slave_id: 从站地址
        :param address: 寄存器地址
        :param value: 写入值
        :return: 是否写入成功
        """
        if client_id in self.rtu_clients:
            client = self.rtu_clients[client_id]
        elif client_id in self.tcp_clients:
            client = self.tcp_clients[client_id]
        else:
            print(f"客户端不存在: {client_id}")
            return False
            
        try:
            result = client.write_register(address, value, slave_id)
            if result.isError():
                print(f"写寄存器失败: {result}")
                return False
            return True
        except Exception as e:
            print(f"写寄存器异常: {e}")
            return False
        
    def close(self, client_id):
        """
        关闭Modbus连接
        :param client_id: 客户端ID
        """
        if client_id in self.rtu_clients:
            client = self.rtu_clients[client_id]
            client.close()
            del self.rtu_clients[client_id]
            print(f"关闭Modbus RTU客户端: {client_id}")
        elif client_id in self.tcp_clients:
            client = self.tcp_clients[client_id]
            client.close()
            del self.tcp_clients[client_id]
            print(f"关闭Modbus TCP客户端: {client_id}")
        else:
            print(f"客户端不存在: {client_id}")

# 测试代码
if __name__ == "__main__":
    modbus_manager = ModbusManager()
    
    # 测试RTU客户端
    rtu_client = modbus_manager.create_rtu_client("rtu1", "/dev/ttyS4", baudrate=9600)
    if rtu_client:
        if modbus_manager.connect("rtu1"):
            # 读取保持寄存器（假设从站地址1，寄存器地址0，读取2个）
            data = modbus_manager.read_holding_registers("rtu1", 1, 0, 2)
            print(f"读取保持寄存器结果: {data}")
            
            # 关闭连接
            modbus_manager.close("rtu1")