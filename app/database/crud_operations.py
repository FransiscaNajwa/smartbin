from datetime import datetime
from bson import ObjectId
from app.database.mongo_client import db
import bcrypt

# ===============================
# 🧠 USERS COLLECTION
# ===============================

def hash_password(password):
    """Hash password sebelum disimpan ke database"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password, hashed):
    """Cek kecocokan password dengan hash yang tersimpan"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def register_user(username, password, email):
    """Tambah user baru ke database"""
    user = {
        "username": username,
        "password": hash_password(password),
        "email": email,
        "created_at": datetime.utcnow()
    }
    result = db.users.insert_one(user)
    return str(result.inserted_id)

def get_user_by_email(email):
    return db.users.find_one({"email": email})

def get_user_by_username(username):
    return db.users.find_one({"username": username})

def get_user_by_id(user_id):
    return db.users.find_one({"_id": ObjectId(user_id)})

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password(password, user["password"]):
        return user
    return None

def update_user_profile(user_id, email=None, username=None, password=None):
    update_fields = {}
    if email: update_fields["email"] = email
    if username: update_fields["username"] = username
    if password: update_fields["password"] = hash_password(password)

    if update_fields:
        result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
        return result.modified_count > 0
    return False

# ===============================
# ♻️ SENSOR DATA COLLECTION
# ===============================

def insert_sensor_data(device_id, temperature, humidity, value, status, timestamp=None):
    try:
        data = {
            "device_id": device_id,
            "temperature": temperature,
            "humidity": humidity,
            "value": value,
            "status": status,
            "timestamp": timestamp or datetime.now()
        }
        result = db.sensor_data.insert_one(data)
        return str(result.inserted_id)
    except Exception as e:
        print(f"⚠️ [MongoDB] Gagal menyimpan data sensor: {e}")
        return None

def insert_dummy_bundle(device_id, capacity, temperature, humidity, status="normal"):
    ts = datetime.utcnow()
    insert_sensor_data(device_id, "capacity", capacity, "%", status, timestamp=ts)
    insert_sensor_data(device_id, "temperature", temperature, "°C", status, timestamp=ts)
    insert_sensor_data(device_id, "humidity", humidity, "%", status, timestamp=ts)

def get_latest_data(limit=10, device_id=None):
    query = {"device_id": device_id} if device_id else {}
    return list(db.sensor_data.find(query).sort("timestamp", -1).limit(limit))

def get_latest_data_by_type(sensor_type, limit=10, device_id=None):
    query = {"sensor_type": sensor_type}
    if device_id: query["device_id"] = device_id
    return list(db.sensor_data.find(query).sort("timestamp", -1).limit(limit))

def get_sensor_data_by_date(date, device_id=None):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start.replace(hour=23, minute=59, second=59)
    query = {"timestamp": {"$gte": start, "$lte": end}}
    if device_id: query["device_id"] = device_id
    return list(db.sensor_data.find(query))

def delete_sensor_data_by_id(sensor_id):
    return db.sensor_data.delete_one({"_id": ObjectId(sensor_id)}).deleted_count > 0

def delete_all_sensor_data():
    return db.sensor_data.delete_many({}).deleted_count

def get_all_device_ids():
    return db.sensor_data.distinct("device_id")

# ===============================
# 🔔 NOTIFICATIONS COLLECTION
# ===============================

def get_notifications_by_category(category):
    return list(db.notifications.find({"category": category}).sort("timestamp", -1))

def detect_notification(entry):
    """Deteksi kondisi abnormal dari satu data sensor"""
    value = entry["value"]
    sensor_type = entry["sensor_type"]
    timestamp = entry["timestamp"]
    device_id = entry["device_id"]

    if sensor_type == "capacity":
        if value >= 90:
            return {
                "device_id": device_id,
                "category": "kapasitas",
                "level": "penuh",
                "value": value,
                "unit": "%",
                "message": "Tempat sampah penuh. Mohon kosongkan secepatnya.",
                "timestamp": timestamp
            }
        elif value >= 80:
            return {
                "device_id": device_id,
                "category": "kapasitas",
                "level": "hampir penuh",
                "value": value,
                "unit": "%",
                "message": "Tempat sampah hampir penuh. Segera lakukan pengosongan.",
                "timestamp": timestamp
            }

    elif sensor_type == "temperature" and value > 35:
        return {
            "device_id": device_id,
            "category": "suhu",
            "level": "tinggi",
            "value": value,
            "unit": "°C",
            "message": "Suhu melebihi ambang batas. Periksa kemungkinan reaksi kimia.",
            "timestamp": timestamp
        }

    elif sensor_type == "humidity" and value > 85:
        return {
            "device_id": device_id,
            "category": "kelembapan",
            "level": "tinggi",
            "value": value,
            "unit": "%",
            "message": "Kelembapan terlalu tinggi. Periksa kondisi sisa makanan.",
            "timestamp": timestamp
        }

    return None

def generate_notifications_from_sensor_data():
    sensor_data = list(db.sensor_data.find().sort("timestamp", -1))
    new_notifications = []

    for entry in sensor_data:
        notif = detect_notification(entry)
        if notif:
            exists = db.notifications.find_one({
                "device_id": notif["device_id"],
                "category": notif["category"],
                "level": notif["level"],
                "timestamp": notif["timestamp"]
            })
            if not exists:
                new_notifications.append(notif)

    if new_notifications:
        db.notifications.insert_many(new_notifications)
        print(f"✅ {len(new_notifications)} notifikasi baru berhasil disimpan.")
    else:
        print("ℹ️ Tidak ada notifikasi baru yang perlu disimpan.")