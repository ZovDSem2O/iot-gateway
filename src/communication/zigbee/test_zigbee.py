# src/communication/zigbee/test_zigbee.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from communication.zigbee.manager import ZigBeeManager

def test_zigbee():
    # 创建 ZigBee 管理器
    zigbee_manager = ZigBeeManager()
    
    # 连接协调器（串口3）
    if zigbee_manager.add_device('coordinator', '/dev/ttyS3'):
        print("ZigBee 协调器连接成功")
        
        try:
            while True:
                # 读取数据
                data = zigbee_manager.read_data('coordinator')
                if data:
                    print(f"收到数据: {data}")
                
                # 等待 1 秒
                time.sleep(1)
        except KeyboardInterrupt:
            print("测试结束")
        finally:
            zigbee_manager.close()
    else:
        print("ZigBee 协调器连接失败")

if __name__ == "__main__":
    test_zigbee()