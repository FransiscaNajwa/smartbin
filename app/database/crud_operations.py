# app/database/crud_operations.py
from datetime import datetime
from bson import ObjectId
from app.database.mongo_client import db

# ===============================
# 🧠 USERS COLLECTION
# ===============================

def register_user(username, password, email):
    """Tambah user baru ke database"""
    user = {
        "username": username,
        "password": password,  # bisa ditambah hashing nanti
        "email": email,
        "created_at": datetime.utcnow()
    }
    result = db.users.insert_one(user)
    return str(result.inserted_id)

def get_user_by_username(username):
    """Ambil data user berdasarkan username"""
    user = db.users.find_one({"username": username})
    return user

# -------------------------------------------------------------
# 🔐 LOGIN VERIFICATION
# -------------------------------------------------------------
def verify_user(email, password):
    """
    Verifikasi pengguna berdasarkan email dan password.
    Return: user document jika cocok, None jika tidak ditemukan.
    """
    user = db.users.find_one({"email": email, "password": password})
    return user

# ===============================
# ♻️ SENSOR DATA COLLECTION
# ===============================

def insert_sensor_data(sensor_type, value, unit, status):
    """Simpan data sensor (kapasitas, suhu, kelembapan)"""
    data = {
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit,
        "status": status,
        "timestamp": datetime.utcnow()
    }
    result = db.sensor_data.insert_one(data)
    return str(result.inserted_id)

def get_latest_sensor_data(limit=10):
    """Ambil data sensor terbaru"""
    return list(db.sensor_data.find().sort("timestamp", -1).limit(limit))

def delete_sensor_data(sensor_id):
    """Hapus data sensor berdasarkan ID"""
    result = db.sensor_data.delete_one({"_id": ObjectId(sensor_id)})
    return result.deleted_count > 0
