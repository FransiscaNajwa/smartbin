import toml
from pathlib import Path
import logging

# 📁 Lokasi file konfigurasi rahasia
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
SECRETS_PATH = CONFIG_DIR / "secrets.toml"

# 🔒 Validasi file konfigurasi
if not SECRETS_PATH.exists():
    raise FileNotFoundError(f"Konfigurasi tidak ditemukan: {SECRETS_PATH}")

# 📦 Baca konfigurasi dari secrets.toml
secrets = toml.load(SECRETS_PATH)

# 📌 Informasi proyek
PROJECT_NAME = "SmartBin IoT Monitoring System"
VERSION = "1.0.0"

# 📡 Konfigurasi MQTT
mqtt_cfg = secrets.get("mqtt", {})
MQTT_BROKER = mqtt_cfg.get("broker", "broker.hivemq.com")
MQTT_PORT = mqtt_cfg.get("port", 1883)
MQTT_USERNAME = mqtt_cfg.get("username", "")
MQTT_PASSWORD = mqtt_cfg.get("password", "")
MQTT_TOPIC_SUBSCRIBE = mqtt_cfg.get("topic_subscribe", "smartbin/data")
MQTT_KEEPALIVE = mqtt_cfg.get("keepalive", 60)
MQTT_RECONNECT_DELAY = mqtt_cfg.get("reconnect_delay", 5)

# 🗄️ Konfigurasi MongoDB
mongo_cfg = secrets.get("mongodb", {})
MONGO_URI = mongo_cfg.get("uri")
MONGO_DB_NAME = mongo_cfg.get("database", "Sensor")
MONGO_SENSOR_COLLECTION = "sensor_data"
MONGO_USER_COLLECTION = "users"

# 🐞 Mode Debug
DEBUG_MODE = secrets.get("debug", False)

# 🧾 Logging
LOG_LEVEL = "DEBUG" if DEBUG_MODE else "INFO"
logging.basicConfig(level=LOG_LEVEL)

# 🧠 Helper fungsi konfigurasi
def get_mqtt_config():
    return {
        "broker": MQTT_BROKER,
        "port": MQTT_PORT,
        "username": MQTT_USERNAME,
        "password": MQTT_PASSWORD,
        "topic": MQTT_TOPIC_SUBSCRIBE,
        "keepalive": MQTT_KEEPALIVE,
        "reconnect_delay": MQTT_RECONNECT_DELAY
    }

def get_mongo_config():
    return {
        "uri": MONGO_URI,
        "db_name": MONGO_DB_NAME,
        "collections": {
            "sensor_data": MONGO_SENSOR_COLLECTION,
            "user": MONGO_USER_COLLECTION
        }
    }
