import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from communication.zigbee.manager import ZigBeeManager
import time

def test_zigbee():
    zigbee_manager = ZigBeeManager()

    print("\n" + "="*50)
    print("ZigBee 通信测试程序")
    print("="*50)

    port = input("\n请输入 ZigBee 协调器连接的串口端口（如 /dev/ttyS3）：").strip()

    if not port:
        print("端口不能为空！")
        return

    if zigbee_manager.add_device('coordinator', port):
        print("\n✓ ZigBee 协调器连接成功！")
        print("\n开始接收数据（按 Ctrl+C 退出）...\n")

        try:
            while True:
                data = zigbee_manager.read_data('coordinator')
                if data:
                    print(f"[收到数据] {data}")

                    if isinstance(data, dict):
                        if 'temperature' in data:
                            print(f"  温度: {data['temperature']}°C")
                        if 'humidity' in data:
                            print(f"  湿度: {data['humidity']}%")

                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n测试结束")
        finally:
            zigbee_manager.close()
    else:
        print("\n✗ ZigBee 协调器连接失败！")
        print("请检查：")
        print("  1. 串口是否正确连接")
        print("  2. 波特率是否正确（默认 9600）")
        print("  3. 协调器是否正常供电")

if __name__ == "__main__":
    test_zigbee()