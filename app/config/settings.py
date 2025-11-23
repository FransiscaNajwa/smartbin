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

# 🐞 Mode Debug
DEBUG_MODE = secrets.get("debug", False)

# 🧾 Logging
LOG_LEVEL = "DEBUG" if DEBUG_MODE else "INFO"
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ===========================
# 📡 Konfigurasi MQTT
# ===========================
mqtt_cfg = secrets.get("mqtt", {})
MQTT_BROKER = mqtt_cfg.get("broker", "broker.hivemq.com")
MQTT_PORT = mqtt_cfg.get("port", 1883)
MQTT_USERNAME = mqtt_cfg.get("username", "")
MQTT_PASSWORD = mqtt_cfg.get("password", "")
MQTT_TOPIC_SUBSCRIBE = mqtt_cfg.get("topic_subscribe", "smartbin/data")
MQTT_KEEPALIVE = mqtt_cfg.get("keepalive", 60)
MQTT_RECONNECT_DELAY = mqtt_cfg.get("reconnect_delay", 5)

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

# ===========================
# 🗄️ Konfigurasi MongoDB
# ===========================
mongo_cfg = secrets.get("mongodb", {})
MONGO_URI = mongo_cfg.get("uri")
MONGO_DB_NAME = mongo_cfg.get("database", "Sensor")
MONGO_SENSOR_COLLECTION = "sensor_data"
MONGO_USER_COLLECTION = "users"

def get_mongo_config():
    return {
        "uri": MONGO_URI,
        "db_name": MONGO_DB_NAME,
        "collections": {
            "sensor_data": MONGO_SENSOR_COLLECTION,
            "user": MONGO_USER_COLLECTION
        }
    }

# ===========================
# 📲 Konfigurasi Telegram
# ===========================
telegram_cfg = secrets.get("telegram", {})
TELEGRAM_TOKEN = telegram_cfg.get("token", "")
TELEGRAM_CHAT_ID = telegram_cfg.get("chat_id", "")

def get_telegram_config():
    return {
        "token": TELEGRAM_TOKEN,
        "chat_id": TELEGRAM_CHAT_ID
    }

# ===========================
# 📧 Konfigurasi Email
# ===========================
email_cfg = secrets.get("email", {})
EMAIL_SMTP_SERVER = email_cfg.get("smtp_server", "")
EMAIL_SMTP_PORT = email_cfg.get("smtp_port", 587)
EMAIL_SENDER = email_cfg.get("sender_email", "")
EMAIL_PASSWORD = email_cfg.get("sender_password", "")
EMAIL_RECEIVER = email_cfg.get("receiver_email", "")

def get_email_config():
    return {
        "smtp_server": EMAIL_SMTP_SERVER,
        "smtp_port": EMAIL_SMTP_PORT,
        "sender_email": EMAIL_SENDER,
        "sender_password": EMAIL_PASSWORD,
        "receiver_email": EMAIL_RECEIVER
    }

# ===========================
# 🧠 Gabungan Konfigurasi
# ===========================
def get_config():
    return {
        "project_name": PROJECT_NAME,
        "version": VERSION,
        "mqtt": get_mqtt_config(),
        "mongodb": get_mongo_config(),
        "telegram": get_telegram_config(),
        "email": get_email_config()
    }