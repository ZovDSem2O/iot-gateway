import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.database import DataStorage
import time
from datetime import datetime

def test_database():
    print("\n" + "=" * 50)
    print("SQLite 数据库测试程序")
    print("=" * 50)

    storage = DataStorage()
    print("\n[OK] 数据库初始化完成！")

    print("\n" + "-" * 50)
    print("测试1：插入一些测试数据")
    print("-" * 50)

    storage.insert_data(
        device_type="zigbee",
        device_id="dht11_001",
        temperature=25.5,
        humidity=60.0,
        raw_data="[25,60]"
    )
    print("[OK] 插入数据1完成！")

    time.sleep(1)

    storage.insert_data(
        device_type="zigbee",
        device_id="dht11_001",
        temperature=26.0,
        humidity=58.5,
        raw_data="[26,58]"
    )
    print("[OK] 插入数据2完成！")

    time.sleep(1)

    storage.insert_data(
        device_type="modbus",
        device_id="sensor_001",
        temperature=24.5,
        humidity=65.0,
        raw_data="[24,65]"
    )
    print("[OK] 插入数据3完成！")

    print("\n" + "-" * 50)
    print("测试2：查询最新数据")
    print("-" * 50)

    latest = storage.get_latest_data(limit=3)
    print(f"最新3条数据：")
    for i, data in enumerate(latest):
        print(f"{i+1}. 设备类型: {data[1]}, 设备ID: {data[2]}, "
              f"温度: {data[3]}, 湿度: {data[4]}, "
              f"时间: {data[7]}")

    print("\n" + "-" * 50)
    print("测试3：查询指定设备的数据")
    print("-" * 50)

    zigbee_data = storage.get_latest_data(device_type="zigbee", limit=2)
    print(f"ZigBee设备最新2条数据：")
    for i, data in enumerate(zigbee_data):
        print(f"{i+1}. 温度: {data[3]}, 湿度: {data[4]}, "
              f"时间: {data[7]}")

    print("\n" + "-" * 50)
    print("测试4：统计数据总数")
    print("-" * 50)

    count = storage.get_data_count()
    print(f"数据库中总共有 {count} 条数据！")

    print("\n" + "-" * 50)
    print("测试5：查询所有设备")
    print("-" * 50)

    devices = storage.get_all_devices()
    print(f"所有设备：")
    for i, device in enumerate(devices):
        print(f"{i+1}. 设备类型: {device[0]}, 设备ID: {device[1]}")

    print("\n" + "=" * 50)
    print("[OK] 所有测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    test_database()