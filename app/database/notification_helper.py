import requests
import logging
from datetime import datetime, timedelta, timezone
from app.config.settings import secrets
from zoneinfo import ZoneInfo

# ===========================
# 🔍 DETEKSI NOTIFIKASI
# ===========================
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

    # 🗑️ Kapasitas
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

    # 🌡️ Suhu
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

    # 💧 Kelembapan
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

    return notifications if notifications else None

def generate_notifications_from_data(sensor_data: list):
    """Menghasilkan list notifikasi dari kumpulan sensor data."""
    if not sensor_data:
        return []

    all_notifications = []
    for entry in sensor_data:
        detected = detect_notification(entry)
        if detected:
            all_notifications.extend(detected)

    # Urutkan dari terbaru ke terlama
    all_notifications.sort(
        key=lambda x: x.get("timestamp", datetime.min),
        reverse=True
    )
    return all_notifications


# ===========================
# 📲 TELEGRAM NOTIFICATION
# ===========================
TELEGRAM_TOKEN = secrets.get("telegram", {}).get("token")
TELEGRAM_CHAT_ID = secrets.get("telegram", {}).get("chat_id")

def send_telegram_notification(message: str):
    """Kirim pesan ke semua chat_id yang ada di secrets.toml"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Telegram token atau chat_id belum dikonfigurasi.")

    # Pastikan chat_id berupa list
    chat_ids = TELEGRAM_CHAT_ID if isinstance(TELEGRAM_CHAT_ID, list) else [TELEGRAM_CHAT_ID]

    results = []
    for cid in chat_ids:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": cid, "text": message}
        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            results.append(response.json())
        except requests.RequestException as e:
            logging.exception(f"❌ Gagal kirim notifikasi ke chat_id {cid}")
            results.append({"ok": False, "chat_id": cid, "error": str(e)})
    return results

def format_notification_message(notif: dict) -> str:
    """Format notifikasi menjadi pesan multi-baris untuk Telegram."""
    waktu = notif.get("timestamp")
    if isinstance(waktu, str):
        try:
            # coba parse ISO format string
            waktu = datetime.fromisoformat(waktu)
            # kurangi 7 jam
            waktu = waktu - timedelta(hours=7)
        except Exception:
            waktu = None
    if isinstance(waktu, datetime):
        # pastikan waktu dianggap UTC kalau belum ada tzinfo
        if waktu.tzinfo is None:
            waktu = waktu.replace(tzinfo=timezone.utc)
        # konversi ke WIB
        waktu_wib = waktu.astimezone(ZoneInfo("Asia/Jakarta"))
        waktu_str = waktu_wib.strftime("%d %b %Y, %H:%M WIB")
    else:
        waktu_str = "-"
    return (
        f"🚨 SmartBin Alert\n"
        f"📦 Device: {notif['device_id']}\n"
        f"⚠️ {notif['message']}\n"
        f"Level: {notif['value']}{notif['unit']}\n"
        f"⏰ {waktu_str}"
    )