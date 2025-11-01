from datetime import datetime


def detect_notification(entry: dict):
    """
    Deteksi apakah satu data sensor perlu menghasilkan notifikasi.
    Tidak menggunakan database, hanya analisis nilai sensor.
    """
    # Validasi data
    if not isinstance(entry, dict):
        return None

    value = entry.get("value")
    sensor_type = entry.get("sensor_type")
    timestamp = entry.get("timestamp", datetime.utcnow())
    device_id = entry.get("device_id", "unknown_device")

    # Pastikan value valid
    if value is None or sensor_type is None:
        return None

    # 🗑️ Kapasitas
    if sensor_type == "capacity":
        if value >= 90:
            level = "penuh"
            message = "Tempat sampah penuh. Mohon kosongkan secepatnya."
        elif value >= 80:
            level = "hampir penuh"
            message = "Tempat sampah hampir penuh. Segera lakukan pengosongan."
        else:
            return None

        return {
            "device_id": device_id,
            "category": "kapasitas",
            "level": level,
            "value": round(value, 2),
            "unit": "%",
            "message": message,
            "timestamp": timestamp
        }

    # 🌡️ Suhu
    elif sensor_type == "temperature" and value > 35:
        return {
            "device_id": device_id,
            "category": "suhu",
            "level": "tinggi",
            "value": round(value, 2),
            "unit": "°C",
            "message": "Suhu melebihi ambang batas. Periksa kemungkinan reaksi kimia.",
            "timestamp": timestamp
        }

    # 💧 Kelembapan
    elif sensor_type == "humidity" and value > 85:
        return {
            "device_id": device_id,
            "category": "kelembapan",
            "level": "tinggi",
            "value": round(value, 2),
            "unit": "%",
            "message": "Kelembapan terlalu tinggi. Periksa kondisi sisa makanan.",
            "timestamp": timestamp
        }

    return None


def generate_notifications_from_data(sensor_data: list):
    """
    Menghasilkan daftar notifikasi berdasarkan kumpulan data sensor.
    Hasil berupa list of dict (bisa langsung ditampilkan di Streamlit).
    """
    if not sensor_data:
        return []

    notifications = []
    for entry in sensor_data:
        notif = detect_notification(entry)
        if notif:
            notifications.append(notif)

    # Urutkan dari waktu terbaru ke lama
    notifications.sort(key=lambda x: x["timestamp"], reverse=True)
    return notifications
