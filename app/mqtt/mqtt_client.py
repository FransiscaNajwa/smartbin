import paho.mqtt.client as mqtt
import json
import math
import time
import logging
from datetime import datetime
from app.config.settings import get_mqtt_config
from app.database.sensor_crud import insert_sensor_data
from app.database.notification_helper import send_email_notification, format_email_message

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
    """
    Menghitung kapasitas tempat sampah dalam persen berdasarkan jarak sensor ultrasonik.
    Rumus: semakin kecil jarak → semakin penuh.
    """
    if jarak_cm < 0:
        return 0
    kapasitas = ((tinggi_bin_cm - jarak_cm) / tinggi_bin_cm) * 100
    return round(max(0, min(kapasitas, 100)), 2)

# 📥 Proses payload dari MQTT
def handle_payload(payload: dict):
    """Proses data sensor dari MQTT dan simpan ke database + notifikasi."""
    try:
        device_id = payload.get("device_id", "unknown")
        status = payload.get("status", "Normal")

        # Data MQTT tidak punya timestamp, gunakan UTC
        timestamp = datetime.utcnow()

        # Ambil nilai sensor langsung
        temperature = payload.get("temperature")
        humidity = payload.get("humidity")
        distance = payload.get("distance")

        # ---- Proses distance -> value ----
        value = None
        if distance is not None:
            try:
                value = hitung_kapasitas(distance)
            except Exception:
                logging.warning("⚠️ Gagal menghitung kapasitas dari distance, set value=None")
                value = None

        # ---- Simpan ke database ----
        insert_sensor_data(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            value=value,
            status=status,
            timestamp=timestamp
        )

        logging.info(f"✅ Data sensor disimpan untuk perangkat {device_id}")

        # ---- Kirim notifikasi email tambahan ----
        if value is not None and value >= 80:  # contoh threshold
            level = "penuh" if value >= 90 else "hampir penuh"
            message = "Tempat sampah penuh. Mohon kosongkan secepatnya." if level == "penuh" else "Tempat sampah hampir penuh. Segera lakukan pengosongan."
            
            body = format_email_message({
                "device_id": device_id,
                "category": "kapasitas",
                "level": level,
                "value": value,
                "unit": "%",
                "message": message,
                "timestamp": timestamp
            })
            send_email_notification("SmartBin Alert", body)

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
        raw = msg.payload.decode("utf-8")

        # Parsing JSON lebih aman daripada eval
        payload = json.loads(raw)

        if not isinstance(payload, dict):
            raise ValueError("Payload bukan dictionary valid.")

        # Normalisasi nilai
        def norm(v):
            return None if isinstance(v, float) and (math.isnan(v) or v == -1) else v

        payload["temperature"] = norm(payload.get("temperature"))
        payload["humidity"]    = norm(payload.get("humidity"))
        payload["distance"]    = norm(payload.get("distance"))

        handle_payload(payload)

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

if __name__ == "__main__":
    client = create_mqtt_client()
    client.loop_forever()