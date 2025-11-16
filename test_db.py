import sys, os

# Tambahkan path root proyek ke sys.path agar bisa import modul internal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# 🔄 Import fungsi dari modul yang sudah dipisah
from app.database.user_crud import register_user, get_user_by_username
from app.database.sensor_crud import insert_sensor_data, get_latest_sensor_data
from app.database.notification_helper import insert_notification, get_latest_notifications

# 🧪 Test registrasi user
print("🧩 Testing user registration...")
user_id = register_user("test_user", "12345", "test@mail.com")
print("✅ New user ID:", user_id)

user = get_user_by_username("test_user")
print("✅ Found user:", user["username"])

# 🧪 Test insert data sensor
print("🧩 Testing sensor data insert...")
data_id = insert_sensor_data("kapasitas", 80, "%", "hampir penuh")
print("✅ Inserted data ID:", data_id)

latest_sensor = get_latest_sensor_data(3)
print("✅ Latest sensor data:", latest_sensor)

# 🧪 Test insert notifikasi
print("🧩 Testing notification insert...")
notif_id = insert_notification("sensor", "Kapasitas hampir penuh", "warning")
print("✅ Notification ID:", notif_id)

latest_notif = get_latest_notifications(3)
print("✅ Latest notifications:", latest_notif)