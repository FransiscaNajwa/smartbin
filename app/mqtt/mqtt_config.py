# app/mqtt/mqtt_config.py

import toml
import os

# ===============================
# 📁 Path ke secrets.toml
# ===============================
SECRETS_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "secrets.toml")

# ===============================
# 🔐 Load konfigurasi dari TOML
# ===============================
try:
    secrets = toml.load(SECRETS_PATH)
    mqtt_secrets = secrets.get("mqtt", {})
except Exception as e:
    raise RuntimeError(f"❌ Gagal membaca secrets.toml: {e}")

# ===============================
# ⚙️ MQTT Configuration Dictionary
# ===============================
MQTT_CONFIG = {
    "BROKER": mqtt_secrets.get("broker", "localhost"),
    "PORT": mqtt_secrets.get("port", 1883),
    "USERNAME": mqtt_secrets.get("username", ""),
    "PASSWORD": mqtt_secrets.get("password", ""),
    "TOPIC_SUBSCRIBE": mqtt_secrets.get("topic_subscribe", "smartbin/data"),
}