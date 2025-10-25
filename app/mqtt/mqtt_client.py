import paho.mqtt.client as mqtt
from app.mqtt.mqtt_config import MQTT_CONFIG
from app.database.crud_operations import insert_sensor_data
import json
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# ===============================
# 🔧 Utility: Hitung Kapasitas dari Jarak
# ===============================
def hitung_kapasitas(jarak_cm, tinggi_bin_cm=40):
    kapasitas = 100 - (jarak_cm / tinggi_bin_cm * 100)
    return round(max(0, min(kapasitas, 100)), 2)

# ===============================
# 📥 Handle Incoming Payload
# ===============================
def handle_payload(payload):
    device_id = payload.get("device_id", "unknown")
    status = payload.get("status", "Normal")

    if "temperature" in payload:
        insert_sensor_data(device_id, "temperature", payload["temperature"], "°C", status)

    if "humidity" in payload:
        insert_sensor_data(device_id, "humidity", payload["humidity"], "%", status)

    if "distance" in payload:
        kapasitas = hitung_kapasitas(payload["distance"])
        insert_sensor_data(device_id, "capacity", kapasitas, "%", status)

    logging.info(f"✅ Sensor data saved for {device_id}")

# ===============================
# 🔌 MQTT CALLBACKS
# ===============================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("✅ MQTT Connected to broker!")
        client.subscribe(MQTT_CONFIG["TOPIC_SUBSCRIBE"])
    else:
        logging.error(f"❌ MQTT Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        handle_payload(payload)
    except Exception as e:
        logging.error(f"❌ Failed to process message: {e}")

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
            logging.info("🔗 Connecting to MQTT broker...")
            client.connect(MQTT_CONFIG["BROKER"], MQTT_CONFIG["PORT"], keepalive=60)
            break
        except Exception as e:
            logging.warning(f"⚠️ Connection failed: {e}, retrying in 5s...")
            time.sleep(5)

    return client

# ===============================
# 📤 PUBLISH GENERIC EVENT
# ===============================
def publish_event(topic, payload):
    try:
        client = create_mqtt_client()
        client.loop_start()
        client.publish(topic, json.dumps(payload))
        logging.info(f"📡 Published event to {topic}: {payload}")
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        logging.error(f"⚠️ Failed to publish event: {e}")

# ===============================
# 📤 PUBLISH SENSOR DATA
# ===============================
def publish_sensor_data(client, sensor_type, value, unit, status):
    payload = {
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit,
        "status": status
    }
    client.publish(MQTT_CONFIG["TOPIC_PUBLISH"], json.dumps(payload))
    logging.info(f"📤 Published sensor data: {payload}")

# ===============================
# 👤 PUBLISH LOGIN EVENT
# ===============================
def publish_login_event(username):
    payload = {
        "event": "login",
        "username": username,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    topic = MQTT_CONFIG.get("TOPIC_LOGIN", "smartbin/login")
    publish_event(topic, payload)