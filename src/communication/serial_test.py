import serial
import time

class SerialPort:
    ##############   串口通信类

    def __init__(self, port, baudrate=9600, timeout=1) -> None:
        """
        初始化串口
        :param port: 串口设备路径
        :param baudrate: 波特率
        :param timeout: 超时时间
        """

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        """打开串口"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout
            )
            print(f"成功打开串口: {self.port}")
        except Exception as e:
            print(f"串口打开失败: {e}")
            return False
        return True

    def close(self):
            """关闭串口"""
            if self.ser:
                self.ser.close()
                print(f"成功关闭串口: {self.port}")
            else:
                print("串口未打开")

    def write(self, data):
        """
        发送数据
        :param data: 要发送的数据（字节）
        :return: 发送的字节数
        """

        if self.ser:
            self.ser.write(data)
            print(f"成功写入数据: {data}")
        else:
            print("串口未打开")
       
    def read(self):
        """
        读取数据
        :param size: 要读取的字节数
        :return: 读取的数据（字节）
        """
        if self.ser:
            data = self.ser.readline().decode().strip()
            print(f"成功读取数据: {data}")
            return data
        else:
            print("串口未打开")
            return None
        
    def read_all(self):
        """
        读取所有可用数据
        :return: 读取的数据（字节）
        """
        if self.ser:
            data = self.ser.read().decode().strip()
            print(f"成功读取所有数据: {data}")
            return data
        else:
            print("串口未打开")
            return None

    def in_waiting(self):
        """
        获取接收缓冲区中的字节数
        :return: 字节数
        """
        if not self.ser or not self.ser.is_open:
            return 0

        try:
            return self.ser.in_waiting

        except Exception as e:
            print(f"获取缓冲区数据失败: {e}")
            return 0

if __name__ == "__main__":
    # 创建串口实例
    serial_port = SerialPort('/dev/ttyS4', baudrate=9600, timeout=1)

    # 打开串口
    if serial_port.open():
        # 发送数据
        serial_port.write(b"Hello, World!\n")
        # 读取数据
        data = serial_port.read()
        if data:
            print(f"收到数据: {data}")
        # 关闭串口
        serial_port.close()
    else:
        print("串口打开失败")