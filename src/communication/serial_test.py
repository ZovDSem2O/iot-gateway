import serial
import time

def test_serial_port(port, baudrate=9600, timeout=1):
    """测试串口通信"""
    try:
        # 打开串口
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout
        )
        print(f"成功打开串口: {port}")
        
        # 测试发送数据
        test_data = b"Hello, Serial!\r\n"
        ser.write(test_data)
        print(f"发送数据: {test_data}")
        
        # 等待接收数据
        time.sleep(0.5)
        if ser.in_waiting > 0:
            received_data = ser.read(ser.in_waiting)
            print(f"接收到数据: {received_data}")
        else:
            print("未接收到数据")
        
        # 关闭串口
        ser.close()
        print("串口测试完成")
        return True
    except Exception as e:
        print(f"串口测试失败: {e}")
        return False

if __name__ == "__main__":
    # 测试RS232串口（假设为/dev/ttyS3）
    print("测试RS232串口...")
    test_serial_port("/dev/ttyS3")
    
    # 测试RS485串口（假设为/dev/ttyUSB0）
    print("\n测试RS485串口...")
    test_serial_port("/dev/ttyUSB0")