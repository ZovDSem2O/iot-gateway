class Notifier:
    def __init__(self):
        pass
    
    def send_alert(self, device_type, device_id, alert_type, alert_message):
        """
        发送告警通知
        """
        print(f"【告警】[{device_type}] 设备 {device_id}")
        print(f"类型: {alert_type}")
        print(f"信息: {alert_message}")
        print("------------------------")
    
    def send_info(self, message):
        """
        发送普通信息通知
        """
        print(f"【信息】{message}")
    
    def send_error(self, message):
        """
        发送错误通知
        """
        print(f"【错误】{message}")