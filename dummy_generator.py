from datetime import datetime
from app.database.sensor_crud import insert_sensor_data
import random
import time

DEVICE_ID = "bin001"
DATA_COUNT = 5   # jumlah data dummy
DELAY = 1        # jeda antar data (detik)

def status_kapasitas(value):
    if value >= 90:
        return "Penuh"
    elif value >= 80:
        return "Hampir Penuh"
    elif value >= 50:
        return "Cukup"
    else:
        return "Rendah"

def status_suhu(value):
    return "Tinggi" if value > 35 else "Normal"

def status_kelembapan(value):
    return "Tinggi" if value > 85 else "Normal"

def generate_dummy_data():
    print(f"🚀 Mulai generate {DATA_COUNT} data dummy untuk perangkat {DEVICE_ID}...\n")

    for i in range(DATA_COUNT):
        timestamp = datetime.utcnow()

        # Data dummy acak
        capacity = round(random.uniform(60, 100), 2)
        temperature = round(random.uniform(30, 38), 2)
        humidity = round(random.uniform(50, 90), 2)

        # Tentukan status otomatis
        cap_status = status_kapasitas(capacity)
        temp_status = status_suhu(temperature)
        hum_status = status_kelembapan(humidity)

        # Simpan ke database
        insert_sensor_data(DEVICE_ID, "capacity", capacity, "%", cap_status, timestamp)
        insert_sensor_data(DEVICE_ID, "temperature", temperature, "°C", temp_status, timestamp)
        insert_sensor_data(DEVICE_ID, "humidity", humidity, "%", hum_status, timestamp)

        print(f"✅ Data {i+1} disimpan:")
        print(f"   🗑️ Kapasitas   : {capacity}%  → Status: {cap_status}")
        print(f"   🌡️ Suhu        : {temperature}°C → Status: {temp_status}")
        print(f"   💧 Kelembapan  : {humidity}% → Status: {hum_status}")
        print("-" * 40)

        time.sleep(DELAY)

    print(f"\n🎉 Selesai generate {DATA_COUNT} data dummy untuk {DEVICE_ID}.")

if __name__ == "__main__":
    generate_dummy_data()
