from pymongo import MongoClient
import certifi
from app.config.settings import *

print("✅ MQTT Broker:", MQTT_BROKER)
print("✅ MQTT Port:", MQTT_PORT)
print("✅ MongoDB URI:", MONGO_URI)
print("✅ Database Name:", MONGO_DB_NAME)

print("\n🔍 Testing MongoDB connection...")
try:
    client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
    client.admin.command("ping")
    print("✅ Koneksi MongoDB berhasil!")
except Exception as e:
    print("❌ Gagal konek MongoDB:", e)
