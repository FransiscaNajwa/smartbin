# app/mqtt/mqtt_config.py
import toml
import os

# Path ke secrets.toml
SECRETS_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "secrets.toml")

secrets = toml.load(SECRETS_PATH)

MQTT_CONFIG = {
    "BROKER": secrets["mqtt"]["broker"],
    "PORT": secrets["mqtt"]["port"],
    "USERNAME": secrets["mqtt"]["username"],
    "PASSWORD": secrets["mqtt"]["password"],
    "TOPIC_PUBLISH": "SmartBin/data",
    "TOPIC_SUBSCRIBE": "SmartBin/control"
}
