import time
from .mqtt_client import MQTTClient

class HuaweiCloudIoT:
    def __init__(self, server_uri, port, device_id, device_secret):
        self.server_uri = server_uri
        self.port = port
        self.device_id = device_id
        self.device_secret = device_secret
        self.mqtt_client = None
        self.username = device_id
        self.password = device_secret

    def connect(self):
        self.mqtt_client = MQTTClient(
            broker=self.server_uri,
            port=self.port,
            username=self.username,
            password=self.password,
            client_id=self.device_id
        )
        return self.mqtt_client.connect()

    def disconnect(self):
        if self.mqtt_client:
            self.mqtt_client.disconnect()

    def publish_properties(self, properties):
        topic = f"$oc/devices/{self.device_id}/sys/properties/report"
        return self.mqtt_client.publish(topic, properties)

    def publish_messages(self, messages):
        topic = f"$oc/devices/{self.device_id}/sys/messages/up"
        return self.mqtt_client.publish(topic, messages)

    def subscribe_commands(self, callback):
        topic = f"$oc/devices/{self.device_id}/sys/commands/#"
        self.mqtt_client.set_message_callback(callback)
        self.mqtt_client.subscribe(topic)

    def is_connected(self):
        return self.mqtt_client and self.mqtt_client.is_connected()

    def on_command(self, topic, data):
        print(f"[华为云] 收到命令: {topic}")
        print(f"[华为云] 命令数据: {data}")
        return data
