from ..modbus import ModbusManager

class TemperatureHumiditySensor:
    """温湿度传感器类"""
    
    def __init__(self, client_id, port, slave_id=1, baudrate=9600):
        """
        初始化温湿度传感器
        :param client_id: 客户端ID
        :param port: 串口设备路径
        :param slave_id: 从站地址
        :param baudrate: 波特率
        """
        self.client_id = client_id
        self.slave_id = slave_id
        self.modbus_manager = ModbusManager()
        self.modbus_manager.create_rtu_client(client_id, port, baudrate)
        
    def connect(self):
        """连接传感器"""
        return self.modbus_manager.connect(self.client_id)
        
    def read_data(self):
        """
        读取温湿度数据
        :return: 温湿度数据字典
        """
        # 读取保持寄存器，地址0，读取2个寄存器
        data = self.modbus_manager.read_holding_registers(
            self.client_id, self.slave_id, 0, 2
        )
        
        if data and len(data) == 2:
            # 湿度值：data[0]
            humidity = data[0] / 10.0  # 转换为%RH
            
            # 温度值：data[1]，处理负数（补码）
            temperature = data[1]
            if temperature > 32767:  # 16位补码，大于32767表示负数
                temperature = (temperature - 65536) / 10.0
            else:
                temperature = temperature / 10.0  # 转换为℃
                
            return {
                'temperature': temperature,
                'humidity': humidity
            }
        return None
        
    def close(self):
        """关闭连接"""
        self.modbus_manager.close(self.client_id)