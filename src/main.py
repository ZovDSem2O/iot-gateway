from communication.sensors.temperature_humidity import TemperatureHumiditySensor
from config.devices import DEVICES

def main():
    """主函数"""
    # 初始化温湿度传感器
    th_config = DEVICES['temperature_humidity']
    sensor = TemperatureHumiditySensor(
        client_id=th_config['client_id'],
        port=th_config['port'],
        slave_id=th_config['slave_id'],
        baudrate=th_config['baudrate']
    )
    
    # 连接传感器
    if sensor.connect():
        print("传感器连接成功")
        
        # 读取数据
        data = sensor.read_data()
        if data:
            print(f"温度: {data['temperature']} ℃")
            print(f"湿度: {data['humidity']} %RH")
        else:
            print("读取数据失败")
            
        # 关闭连接
        sensor.close()
    else:
        print("传感器连接失败")

if __name__ == "__main__":
    main()