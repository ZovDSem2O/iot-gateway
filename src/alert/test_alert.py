import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alert.anomaly_detector import AnomalyDetector
from alert.alert_manager import AlertManager
from alert.notifier import Notifier


def test_anomaly_detector():
    print("测试异常检测模块...")
    detector = AnomalyDetector()
    
    # 测试正常温度
    result = detector.check(temperature=25, humidity=60)
    print(f"正常数据测试: {result}")
    
    # 测试温度过高
    result = detector.check(temperature=85, humidity=60)
    print(f"温度过高测试: {result}")
    
    # 测试温度过低
    result = detector.check(temperature=-5, humidity=60)
    print(f"温度过低测试: {result}")
    
    # 测试湿度过高
    result = detector.check(temperature=25, humidity=95)
    print(f"湿度过高测试: {result}")
    
    # 测试湿度过低
    result = detector.check(temperature=25, humidity=15)
    print(f"湿度过低测试: {result}")
    
    print("异常检测模块测试完成！")
    print("------------------------")


def test_alert_manager():
    print("测试告警管理模块...")
    manager = AlertManager()
    
    # 保存一条告警
    manager.save_alert(
        device_type='zigbee',
        device_id='dht11_001',
        alert_type='温度过高',
        alert_message='温度过高: 85°C (正常: 0-80°C)',
        temperature=85.0,
        humidity=60.0
    )
    print("告警已保存！")
    
    # 获取未处理告警
    alerts = manager.get_unresolved_alerts()
    print(f"未处理告警数量: {len(alerts)}")
    for alert in alerts:
        print(f"告警: ID={alert[0]}, 设备={alert[2]}, 类型={alert[3]}, 时间={alert[8]}")
    
    print("告警管理模块测试完成！")
    print("------------------------")


def test_notifier():
    print("测试通知系统...")
    notifier = Notifier()
    
    notifier.send_alert(
        device_type='zigbee',
        device_id='dht11_001',
        alert_type='温度过高',
        alert_message='温度过高: 85°C'
    )
    
    notifier.send_info('系统运行正常')
    notifier.send_error('连接失败')
    
    print("通知系统测试完成！")
    print("------------------------")


def test_integration():
    print("测试完整告警流程...")
    
    # 创建对象
    detector = AnomalyDetector()
    manager = AlertManager()
    notifier = Notifier()
    
    # 模拟传感器数据
    temperature = 90  # 异常！
    humidity = 50
    
    # 检测异常
    anomalies = detector.check(temperature=temperature, humidity=humidity)
    
    if anomalies:
        print(f"检测到异常: {anomalies}")
        
        # 保存告警
        for anomaly in anomalies:
            manager.save_alert(
                device_type='zigbee',
                device_id='dht11_001',
                alert_type='温度异常',
                alert_message=anomaly,
                temperature=temperature,
                humidity=humidity
            )
        
        # 发送通知
        notifier.send_alert(
            device_type='zigbee',
            device_id='dht11_001',
            alert_type='温度异常',
            alert_message=anomalies[0]
        )
    else:
        print("数据正常！")
    
    print("完整告警流程测试完成！")


if __name__ == "__main__":
    test_anomaly_detector()
    test_alert_manager()
    test_notifier()
    test_integration()