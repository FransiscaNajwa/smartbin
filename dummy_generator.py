from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from app.mqtt.mqtt_config import secrets

client = MongoClient(secrets["mongodb"]["uri"])
db = client[secrets["mongodb"]["database"]]
collection = db["sensor_data"]

def generate_dummy_data(device_id="bin001", offset_minutes=0):
    suhu = round(random.uniform(28, 35), 2)
    kelembapan = round(random.uniform(50, 80), 2)
    kapasitas = round(random.uniform(10, 95), 2)
    status = "Normal" if kapasitas < 80 else "Hampir Penuh"

    timestamp = datetime.utcnow() - timedelta(minutes=offset_minutes)

    dummy_entries = [
        {
            "device_id": device_id,
            "sensor_type": "temperature",
            "value": suhu,
            "unit": "°C",
            "status": status,
            "timestamp": timestamp
        },
        {
            "device_id": device_id,
            "sensor_type": "humidity",
            "value": kelembapan,
            "unit": "%",
            "status": status,
            "timestamp": timestamp
        },
        {
            "device_id": device_id,
            "sensor_type": "capacity",
            "value": kapasitas,
            "unit": "%",
            "status": status,
            "timestamp": timestamp
        }
    ]

    collection.insert_many(dummy_entries)
    print(f"✅ Data dummy untuk {device_id} @ {timestamp.strftime('%H:%M')}")

if __name__ == "__main__":
    device_ids = [f"bin{str(i).zfill(3)}" for i in range(1, 11)]  # bin001–bin010

    for batch in range(10):  # 10 waktu berbeda
        for device_id in device_ids:
            generate_dummy_data(device_id, offset_minutes=batch * 5)

    print("✅ 300 data dummy berhasil ditambahkan ke MongoDB.")