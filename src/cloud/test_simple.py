import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

print("Testing MQTT module import...")
try:
    from src.cloud.mqtt_client import MQTTClient
    print("[OK] Import successful!")
    
    print("\nCreating MQTT client...")
    client = MQTTClient(
        broker="test.mosquitto.org",
        port=1883,
        username="",
        password="",
        client_id="test_client"
    )
    print("[OK] Client created!")
    
    print("\nTesting connect...")
    result = client.connect()
    print("Connect result:", result)
    
    import time
    time.sleep(1)
    print("Connected status:", client.is_connected())
    
    client.disconnect()
    print("[OK] Disconnected!")
    
except Exception as e:
    print("[ERROR]", str(e))
    import traceback
    traceback.print_exc()