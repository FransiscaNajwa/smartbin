import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.mqtt.mqtt_client import create_mqtt_client, publish_sensor_data

client = create_mqtt_client()
client.loop_start()

# Kirim contoh data SmartBin
publish_sensor_data(client, "kelembapan", 60, "%", "normal")

# Tunggu pesan masuk
import time
time.sleep(5)

client.loop_stop()
client.disconnect()
