from datetime import datetime, timezone, timedelta
from bson import ObjectId
from app.database.mongo_client import db
from app.config.settings import MONGO_SENSOR_COLLECTION

def ensure_db():
    """Pastikan koneksi database aktif sebelum melakukan operasi."""
    if db is None:
        raise ConnectionError("❌ Database belum terhubung. Pastikan MongoDB aktif.")

def insert_sensor_data(device_id, temperature, humidity, value, status, timestamp=None):
    WIB = timezone(timedelta(hours=7))
    """Masukkan 1 data sensor ke MongoDB."""
    ensure_db()
    data = {
            "device_id": device_id,
            "temperature": temperature,
            "humidity": humidity,
            "value": value,
            "status": status,
            "timestamp": timestamp or datetime.now(WIB)
        }
    result = db[MONGO_SENSOR_COLLECTION].insert_one(data)
    return str(result.inserted_id)

# def insert_dummy_bundle(device_id, capacity, temperature, humidity, status="normal"):
#     """Masukkan 3 data sensor sekaligus untuk simulasi."""
#     ts = datetime.utcnow()
#     insert_sensor_data(device_id, "capacity", capacity, "%", status, timestamp=ts)
#     insert_sensor_data(device_id, "temperature", temperature, "°C", status, timestamp=ts)
#     insert_sensor_data(device_id, "humidity", humidity, "%", status, timestamp=ts)
#     return True  # biar tahu fungsinya berhasil

def get_latest_data(limit=10, device_id=None):
    """Ambil data sensor terbaru (umum)."""
    ensure_db()
    query = {"device_id": device_id} if device_id else {}
    cursor = db[MONGO_SENSOR_COLLECTION].find(query).sort("timestamp", -1).limit(limit)
    return list(cursor)

def get_latest_data_by_type(sensor_type, limit=10, device_id=None):
    """Ambil data sensor terbaru berdasarkan jenis sensor."""
    ensure_db()
    query = {"sensor_type": sensor_type}
    if device_id:
        query["device_id"] = device_id
    cursor = db[MONGO_SENSOR_COLLECTION].find(query).sort("timestamp", -1).limit(limit)
    return list(cursor)

def get_sensor_data_by_date(date, device_id=None):
    """Ambil data sensor berdasarkan tanggal (YYYY-MM-DD)."""
    ensure_db()
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start.replace(hour=23, minute=59, second=59)
    query = {"timestamp": {"$gte": start, "$lte": end}}
    if device_id:
        query["device_id"] = device_id
    cursor = db[MONGO_SENSOR_COLLECTION].find(query).sort("timestamp", -1)
    return list(cursor)

def delete_sensor_data_by_id(sensor_id):
    """Hapus data sensor berdasarkan ID."""
    ensure_db()
    result = db[MONGO_SENSOR_COLLECTION].delete_one({"_id": ObjectId(sensor_id)})
    return result.deleted_count > 0

def delete_all_sensor_data():
    """Hapus semua data sensor di koleksi."""
    ensure_db()
    result = db[MONGO_SENSOR_COLLECTION].delete_many({})
    return result.deleted_count

def get_all_device_ids():
    """Ambil semua ID perangkat unik."""
    ensure_db()
    return db[MONGO_SENSOR_COLLECTION].distinct("device_id")
