import sys, os

# Tambahkan path root proyek ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.database.crud_operations import (
    register_user, get_user_by_username,
    insert_sensor_data, get_latest_sensor_data
)

print("🧩 Testing user registration...")
user_id = register_user("test_user", "12345", "test@mail.com")
print("✅ New user ID:", user_id)

user = get_user_by_username("test_user")
print("✅ Found user:", user["username"])

print("🧩 Testing sensor data insert...")
data_id = insert_sensor_data("kapasitas", 80, "%", "hampir penuh")
print("✅ Inserted data ID:", data_id)

latest = get_latest_sensor_data(3)
print("✅ Latest sensor data:", latest)
