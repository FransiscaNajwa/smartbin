# app/config/settings.py

import toml
from pathlib import Path

# 📁 Lokasi file konfigurasi rahasia
BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_PATH = BASE_DIR / "config" / "secrets.toml"

# 🔒 Validasi file konfigurasi
if not SECRETS_PATH.exists():
    raise FileNotFoundError(f"Konfigurasi tidak ditemukan di {SECRETS_PATH}")

# 📦 Baca konfigurasi dari secrets.toml
secrets = toml.load(SECRETS_PATH)

# 📌 Informasi proyek
PROJECT_NAME = "SmartBin IoT Monitoring System"
VERSION = "1.0.0"

# 📡 Konfigurasi MQTT
MQTT_BROKER = secrets["mqtt"]["broker"]
MQTT_PORT = secrets["mqtt"]["port"]
MQTT_USERNAME = secrets["mqtt"]["username"]
MQTT_PASSWORD = secrets["mqtt"]["password"]
MQTT_TOPIC_SUBSCRIBE = secrets["mqtt"]["topic_subscribe"]

# 🗄️ Konfigurasi MongoDB
MONGO_URI = secrets["mongodb"]["uri"]
MONGO_DB_NAME = secrets["mongodb"]["database"]
MONGO_SENSOR_COLLECTION = "sensor_data"
MONGO_USER_COLLECTION = "users"

# 🌐 Konfigurasi Flask
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# 🐞 Mode Debug
DEBUG_MODE = True