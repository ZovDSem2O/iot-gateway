import sqlite3
import time
from datetime import datetime

print("\n" + "=" * 50)
print("SQLite 数据库演示程序")
print("=" * 50)

print("\n" + "-" * 50)
print("第一步：连接数据库（自动创建）")
print("-" * 50)

conn = sqlite3.connect("gateway_data.db")
cursor = conn.cursor()
print("[OK] 数据库连接成功！")

print("\n" + "-" * 50)
print("第二步：创建 sensor_data 表")
print("-" * 50)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_type TEXT NOT NULL,
        device_id TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        raw_data TEXT,
        timestamp TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
''')
conn.commit()
print("[OK] 表创建成功！")

print("\n" + "-" * 50)
print("第三步：插入一些测试数据")
print("-" * 50)

now1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cursor.execute('''
    INSERT INTO sensor_data 
    (device_type, device_id, temperature, humidity, raw_data, timestamp, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', ("zigbee", "dht11_001", 25.5, 60.0, "[25,60]", now1, now1))
print("[OK] 插入数据1：温度 25.5°C，湿度 60%")

time.sleep(1)

now2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cursor.execute('''
    INSERT INTO sensor_data 
    (device_type, device_id, temperature, humidity, raw_data, timestamp, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', ("zigbee", "dht11_001", 26.0, 58.5, "[26,58]", now2, now2))
print("[OK] 插入数据2：温度 26.0°C，湿度 58.5%")

time.sleep(1)

now3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cursor.execute('''
    INSERT INTO sensor_data 
    (device_type, device_id, temperature, humidity, raw_data, timestamp, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', ("modbus", "sensor_001", 24.5, 65.0, "[24,65]", now3, now3))
print("[OK] 插入数据3：温度 24.5°C，湿度 65%")

conn.commit()

print("\n" + "-" * 50)
print("第四步：查询最新数据")
print("-" * 50)

cursor.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 3')
result = cursor.fetchall()
print(f"最新3条数据：")
for i, data in enumerate(result):
    print(f"{i+1}. 设备类型: {data[1]}, 设备ID: {data[2]}, "
          f"温度: {data[3]}, 湿度: {data[4]}, "
          f"时间: {data[7]}")

print("\n" + "-" * 50)
print("第五步：查询指定设备的数据")
print("-" * 50)

cursor.execute('SELECT * FROM sensor_data WHERE device_type = "zigbee" ORDER BY id DESC LIMIT 2')
result = cursor.fetchall()
print(f"ZigBee设备最新2条数据：")
for i, data in enumerate(result):
    print(f"{i+1}. 温度: {data[3]}, 湿度: {data[4]}, "
          f"时间: {data[7]}")

print("\n" + "-" * 50)
print("第六步：统计数据总数")
print("-" * 50)

cursor.execute('SELECT COUNT(*) FROM sensor_data')
count = cursor.fetchone()
print(f"数据库中总共有 {count[0]} 条数据！")

print("\n" + "-" * 50)
print("第七步：查询所有设备")
print("-" * 50)

cursor.execute('SELECT DISTINCT device_type, device_id FROM sensor_data')
result = cursor.fetchall()
print(f"所有设备：")
for i, device in enumerate(result):
    print(f"{i+1}. 设备类型: {device[0]}, 设备ID: {device[1]}")

conn.close()
print("\n" + "-" * 50)
print("关闭数据库连接")
print("-" * 50)

print("\n" + "=" * 50)
print("[OK] SQLite 演示完成！")
print("=" * 50)