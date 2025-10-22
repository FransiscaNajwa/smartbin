import paho.mqtt.client as mqtt
from app.mqtt.mqtt_config import MQTT_CONFIG
import json
import time

# ===============================
# 🔌 MQTT CALLBACKS
# ===============================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT Connected to broker!")
        client.subscribe(MQTT_CONFIG["TOPIC_SUBSCRIBE"])
    else:
        print(f"❌ MQTT Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"📩 Received message on {msg.topic}: {msg.payload.decode()}")

# ===============================
# ⚙️ CREATE MQTT CLIENT
# ===============================
def create_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(MQTT_CONFIG["USERNAME"], MQTT_CONFIG["PASSWORD"])
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            print("🔗 Connecting to MQTT broker...")
            client.connect(MQTT_CONFIG["BROKER"], MQTT_CONFIG["PORT"], keepalive=60)
            break
        except Exception as e:
            print(f"⚠️ Connection failed: {e}, retrying in 5s...")
            time.sleep(5)

    return client

# ===============================
# 📡 PUBLISH SENSOR DATA
# ===============================
def publish_sensor_data(client, sensor_type, value, unit, status):
    payload = {
        "type": sensor_type,
        "value": value,
        "unit": unit,
        "status": status
    }
    client.publish(MQTT_CONFIG["TOPIC_PUBLISH"], json.dumps(payload))
    print(f"📤 Published sensor data: {payload}")

# ===============================
# 👤 PUBLISH LOGIN EVENT
# ===============================
def publish_login_event(username):
    """
    Kirim event login user ke broker MQTT.
    """
    try:
        client = create_mqtt_client()
        client.loop_start()

        payload = {
            "event": "login",
            "username": username,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Pastikan ada topik untuk login di konfigurasi
        topic = MQTT_CONFIG.get("TOPIC_LOGIN", "smartbin/login")

        client.publish(topic, json.dumps(payload))
        print(f"📡 Published login event: {payload}")

        # Hentikan koneksi setelah publish
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"⚠️ Failed to publish login event: {e}")

# ===============================
# 🧪 TEST MODE
# ===============================
if __name__ == "__main__":
    client = create_mqtt_client()
    client.loop_start()

    # Contoh publish dummy data
    publish_sensor_data(client, "kapasitas", 75, "%", "hampir penuh")

    # Contoh publish event login
    publish_login_event("caca")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("🛑 MQTT stopped.")
