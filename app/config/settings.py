# app/config/settings.py
import toml
from pathlib import Path

# Lokasi file konfigurasi rahasia
BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_PATH = BASE_DIR / "config" / "secrets.toml"

# Baca konfigurasi rahasia
secrets = toml.load(SECRETS_PATH)

# Informasi proyek
PROJECT_NAME = "SmartBin IoT Monitoring System"
VERSION = "1.0.0"

# MQTT Configuration
MQTT_BROKER = secrets["mqtt"]["broker"]
MQTT_PORT = secrets["mqtt"]["port"]
MQTT_USERNAME = secrets["mqtt"]["username"]
MQTT_PASSWORD = secrets["mqtt"]["password"]
MQTT_TOPIC_PUBLISH = secrets["mqtt"]["topic_publish"]
MQTT_TOPIC_SUBSCRIBE = secrets["mqtt"]["topic_subscribe"]

# MongoDB Configuration
MONGO_URI = secrets["mongodb"]["uri"]
MONGO_DB_NAME = secrets["mongodb"]["database"]
MONGO_SENSOR_COLLECTION = "sensor_data"
MONGO_USER_COLLECTION = "users"

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
