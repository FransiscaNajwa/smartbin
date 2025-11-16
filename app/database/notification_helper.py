from datetime import datetime

def detect_notification(entry: dict):
    """
    Deteksi notifikasi dari satu entry sensor.
    Tidak menggunakan sensor_type karena data tidak memilikinya.
    """
    if not isinstance(entry, dict):
        return None

    timestamp = entry.get("timestamp", datetime.utcnow())
    device_id = entry.get("device_id", "unknown_device")

    notifications = []

    # ===========================
    # 🗑️ KAPASITAS (value)
    # ===========================
    kapasitas = entry.get("value")
    if kapasitas is not None:
        if kapasitas >= 90:
            notifications.append({
                "device_id": device_id,
                "category": "kapasitas",
                "level": "penuh",
                "value": round(kapasitas, 2),
                "unit": "%",
                "message": "Tempat sampah penuh. Mohon kosongkan secepatnya.",
                "timestamp": timestamp
            })
        elif kapasitas >= 80:
            notifications.append({
                "device_id": device_id,
                "category": "kapasitas",
                "level": "hampir penuh",
                "value": round(kapasitas, 2),
                "unit": "%",
                "message": "Tempat sampah hampir penuh. Segera lakukan pengosongan.",
                "timestamp": timestamp
            })

    # ===========================
    # 🌡️ SUHU (temperature)
    # ===========================
    suhu = entry.get("temperature")
    if suhu is not None and suhu > 35:
        notifications.append({
            "device_id": device_id,
            "category": "suhu",
            "level": "tinggi",
            "value": round(suhu, 2),
            "unit": "°C",
            "message": "Suhu melebihi ambang batas. Periksa kemungkinan reaksi kimia.",
            "timestamp": timestamp
        })

    # ===========================
    # 💧 KELEMBAPAN (humidity)
    # ===========================
    kelembapan = entry.get("humidity")
    if kelembapan is not None and kelembapan > 85:
        notifications.append({
            "device_id": device_id,
            "category": "kelembapan",
            "level": "tinggi",
            "value": round(kelembapan, 2),
            "unit": "%",
            "message": "Kelembapan terlalu tinggi. Periksa kondisi sisa makanan.",
            "timestamp": timestamp
        })

    # Jika tidak ada notifikasi → None
    return notifications if notifications else None


def generate_notifications_from_data(sensor_data: list):
    """
    Menghasilkan list notifikasi dari kumpulan sensor data.
    """
    if not sensor_data:
        return []

    all_notifications = []

    for entry in sensor_data:
        detected = detect_notification(entry)
        if detected:
            all_notifications.extend(detected)

    # Urutkan notifikasi dari terbaru ke terlama
    all_notifications.sort(
        key=lambda x: x.get("timestamp", datetime.min),
        reverse=True
    )
    return all_notifications
