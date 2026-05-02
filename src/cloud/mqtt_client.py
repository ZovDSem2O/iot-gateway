import paho.mqtt.client as mqtt
import json
import time

class MQTTClient:
    def __init__(self, broker, port, username, password, client_id):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client = None
        self.connected = False
        self.subscribed_topics = {}
        self.message_callback = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[OK] MQTT connected! Broker:", self.broker, ":", self.port)
            self.connected = True
            for topic in self.subscribed_topics.keys():
                self.client.subscribe(topic)
                print("  Subscribed to:", topic)
        else:
            print("[ERROR] MQTT connect failed! Return code:", rc)
            self.connected = False

    def on_disconnect(self, client, userdata, rc):
        print("[ERROR] MQTT disconnected! Return code:", rc)
        self.connected = False

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            print("[MQTT received] Topic:", topic, ", Data:", payload)
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                data = payload
            if self.message_callback:
                self.message_callback(topic, data)
        except Exception as e:
            print("[MQTT error] Failed to process message:", str(e))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("[MQTT] Subscribed successfully, Message ID:", mid, ", QoS:", granted_qos)

    def connect(self):
        try:
            self.client = mqtt.Client(client_id=self.client_id)
            self.client.reconnect_delay_set(min_delay=1, max_delay=60)
            if self.username:
                self.client.username_pw_set(self.username, self.password)
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            self.client.on_subscribe = self.on_subscribe
            print("Connecting to", self.broker, ":", self.port, "...")
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            return True
        except Exception as e:
            print("[MQTT error] Connect failed:", str(e))
            return False

    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            print("[MQTT] Disconnected")

    def subscribe(self, topic, qos=0):
        if self.connected:
            self.client.subscribe(topic, qos)
            self.subscribed_topics[topic] = qos
            print("[MQTT] Subscribe to:", topic, ", QoS:", qos)
        else:
            print("[MQTT error] Not connected, cannot subscribe to:", topic)

    def publish(self, topic, payload, qos=0):
        if not self.connected:
            print("[MQTT error] Not connected, cannot publish to:", topic)
            return False
        try:
            if isinstance(payload, dict):
                message = json.dumps(payload)
            else:
                message = str(payload)
            result = self.client.publish(topic, message, qos)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("[MQTT publish] Topic:", topic, ", Data:", message)
                return True
            else:
                print("[MQTT error] Publish failed, Return code:", result.rc)
                return False
        except Exception as e:
            print("[MQTT error] Failed to publish:", str(e))
            return False

    def set_message_callback(self, callback):
        self.message_callback = callback

    def is_connected(self):
        return self.connected