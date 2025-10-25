# app/database/mongo_client.py

from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]  # ✅ konsisten dengan secrets.toml dan settings.py