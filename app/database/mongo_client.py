from pymongo import MongoClient
import certifi
from app.config.settings import MONGO_URI, MONGO_DB_NAME

db = None

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )
    client.admin.command("ping")
    db = client[MONGO_DB_NAME]
    print(f"✅ Connected to MongoDB: {MONGO_DB_NAME}")
    print("✅ Collections:", db.list_collection_names())

except Exception as e:
    print("❌ MongoDB connection failed:", e)
    db = None