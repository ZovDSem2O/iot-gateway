import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.cloud.mqtt_client import MQTTClient
import time

def test_mqtt():
    mqtt_client = MQTTClient(
        # broker="test.mosquitto.org",
        broker="broker.emqx.io",
        port=1883,
        username="",
        password="",
        client_id="test_client_001"
    )

    print("\n" + "="*50)
    print("MQTT 通信测试程序")
    print("="*50)

    result = mqtt_client.connect()
    # print("Connect result:", result)
    time.sleep(2)
    print("Connected status:", mqtt_client.is_connected())
    
    if mqtt_client.is_connected():
        print("\n[OK] MQTT 连接成功！")
        print("\n开始测试（按 Ctrl+C 退出）...\n")

        topic = "test/topic"
        mqtt_client.subscribe(topic)
        mqtt_client.publish(topic, {"message": "Hello MQTT", "value": 123})

        try:
            count = 0
            while count < 10:
                mqtt_client.publish(topic, {
                    "temperature": 25.0 + count,
                    "humidity": 60.0 - count,
                    "timestamp": time.time()
                })
                time.sleep(2)
                count += 1
        except KeyboardInterrupt:
            print("\n\n测试结束")
        finally:
            mqtt_client.disconnect()
    else:
        print("\n[ERROR] MQTT 连接失败！")

if __name__ == "__main__":
    test_mqtt()
