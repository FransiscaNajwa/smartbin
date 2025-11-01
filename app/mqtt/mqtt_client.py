import paho.mqtt.client as mqtt
import json
import time
import logging
from datetime import datetime
from app.config.settings import get_mqtt_config
from app.database.sensor_crud import insert_sensor_data
from app.database.notification_helper import detect_notification, insert_notification

# 📦 Load konfigurasi MQTT dari settings.py
MQTT_CONFIG = get_mqtt_config()

# 🧾 Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 🔧 Hitung kapasitas berdasarkan jarak sensor ultrasonik
def hitung_kapasitas(jarak_cm: float, tinggi_bin_cm: float = 40) -> float:
    """Menghitung kapasitas tempat sampah dalam persen berdasarkan jarak sensor ultrasonik."""
    if jarak_cm < 0:
        return 0
    kapasitas = 100 - (jarak_cm / tinggi_bin_cm * 100)
    return round(max(0, min(kapasitas, 100)), 2)

# 📥 Proses payload dari MQTT
def handle_payload(payload: dict):
    """Proses data sensor dari MQTT dan simpan ke database."""
    try:
        device_id = payload.get("device_id", "unknown")
        status = payload.get("status", "Normal")
        timestamp_str = payload.get("timestamp")
        
        # Konversi timestamp ke UTC jika string ISO diberikan
        if isinstance(timestamp_str, str):
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                timestamp = datetime.utcnow()
        else:
            timestamp = datetime.utcnow()

        sensor_types = {
            "temperature": ("°C", "suhu"),
            "humidity": ("%", "kelembapan"),
            "distance": ("%", "kapasitas")
        }

        for key, (unit, category) in sensor_types.items():
            if key not in payload:
                continue

            value = payload[key]
            if value is None:
                logging.warning(f"⚠️ Nilai sensor '{key}' kosong, dilewati.")
                continue

            if key == "distance":
                value = hitung_kapasitas(value)

            # Simpan data sensor
            insert_sensor_data(device_id, category, value, unit, status, timestamp)

            # Deteksi dan simpan notifikasi (jika perlu)
            notif_data = {
                "device_id": device_id,
                "sensor_type": category,
                "value": value,
                "unit": unit,
                "status": status,
                "timestamp": timestamp,
            }
            notif = detect_notification(notif_data)
            if notif and insert_notification(notif):
                logging.info(f"🔔 Notifikasi {category.upper()}: {notif['message']}")

        logging.info(f"✅ Data sensor disimpan untuk perangkat {device_id}")

    except Exception as e:
        logging.exception(f"❌ Gagal memproses payload: {e}")

# 🔌 Callback saat koneksi MQTT berhasil
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("✅ MQTT terhubung ke broker.")
        client.subscribe(MQTT_CONFIG["topic"])
        logging.info(f"📡 Subscribed ke topik: {MQTT_CONFIG['topic']}")
    else:
        logging.error(f"❌ Gagal koneksi MQTT. Kode: {rc}")

# 📩 Callback saat pesan diterima
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Payload bukan dictionary JSON.")
        handle_payload(payload)
    except json.JSONDecodeError:
        logging.error("❌ Format JSON tidak valid pada pesan MQTT.")
    except Exception as e:
        logging.exception(f"❌ Error saat memproses pesan MQTT: {e}")

# ⚙️ Inisialisasi dan koneksi MQTT client
def create_mqtt_client():
    """Buat dan koneksikan MQTT client dengan auto-reconnect."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_CONFIG["username"], MQTT_CONFIG["password"])
    client.on_connect = on_connect
    client.on_message = on_message

    connected = False
    while not connected:
        try:
            logging.info("🔗 Menghubungkan ke broker MQTT...")
            client.connect(
                MQTT_CONFIG["broker"],
                MQTT_CONFIG["port"],
                keepalive=MQTT_CONFIG.get("keepalive", 60)
            )
            connected = True
        except Exception as e:
            delay = MQTT_CONFIG.get("reconnect_delay", 5)
            logging.warning(f"⚠️ Gagal koneksi: {e}. Coba lagi dalam {delay} detik...")
            time.sleep(delay)

    return client
