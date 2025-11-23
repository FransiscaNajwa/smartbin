import requests
import smtplib
import logging
from email.mime.text import MIMEText
from datetime import datetime
from app.config.settings import secrets, get_email_config

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
    """Kirim pesan ke Telegram. Return dict hasil API."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Telegram token atau chat_id belum dikonfigurasi.")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.exception("❌ Gagal kirim notifikasi Telegram")
        return {"ok": False, "error": str(e)}


def format_notification_message(notif: dict) -> str:
    """Format notifikasi menjadi pesan multi-baris untuk Telegram."""
    waktu = notif.get("timestamp")
    waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if isinstance(waktu, datetime) else "-"
    return (
        f"🚨 SmartBin Alert\n"
        f"📦 Device: {notif['device_id']}\n"
        f"⚠️ {notif['message']}\n"
        f"Level: {notif['value']}{notif['unit']}\n"
        f"⏰ {waktu_str}"
    )


# ===========================
# 📧 EMAIL NOTIFICATION
# ===========================
def format_email_message(notif: dict) -> str:
    """Format notifikasi menjadi pesan multi-baris untuk Email."""
    waktu = notif.get("timestamp")
    waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if isinstance(waktu, datetime) else "-"
    return (
        f"SmartBin Alert\n\n"
        f"Device: {notif['device_id']}\n"
        f"Kategori: {notif['category']}\n"
        f"Level: {notif['level']}\n"
        f"Nilai: {notif['value']}{notif['unit']}\n"
        f"Pesan: {notif['message']}\n"
        f"Waktu: {waktu_str}\n"
    )

def send_email_notification(subject: str, body: str):
    """Kirim notifikasi via Email menggunakan SMTP."""
    cfg = get_email_config()
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = cfg["sender_email"]
    msg["To"] = cfg["receiver_email"]

    try:
        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["sender_email"], cfg["sender_password"])
            server.send_message(msg)
        return {"ok": True}
    except Exception as e:
        logging.exception("❌ Gagal kirim email notifikasi")
        return {"ok": False, "error": str(e)}