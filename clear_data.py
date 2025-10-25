from pymongo import MongoClient
from app.mqtt.mqtt_config import secrets

# Koneksi ke MongoDB
client = MongoClient(secrets["mongodb"]["uri"])
db = client[secrets["mongodb"]["database"]]
collection = db["sensor_data"]

# Hapus semua data
result = collection.delete_many({})

# Tampilkan hasil
print(f"✅ {result.deleted_count} data berhasil dihapus dari koleksi sensor_data.")