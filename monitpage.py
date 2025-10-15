import streamlit as st
import paho.mqtt.client as mqtt
import json
import threading
import pymongo
from datetime import datetime
import altair as alt
import pandas as pd

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/smartbin_db")
db = client.smartbin_db
sensors = db.sensors

# MQTT Konfigurasi (HiveMQ)
HIVEMQ_BROKER = "your-hivemq-broker.com"
HIVEMQ_PORT = 1883
HIVEMQ_USER = "user"
HIVEMQ_PASS = "pass"
MQTT_TOPIC = "smartbin/sensor/#"

# State untuk data real-time
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {"kapasitas": 0, "suhu": 0, "kelembapan": 0}

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic_parts = msg.topic.split("/")
    if len(topic_parts) > 2:
        sensor_type = topic_parts[2]
        st.session_state.sensor_data[sensor_type] = payload["value"]
        # Simpan ke MongoDB
        sensors.insert_one({"type": sensor_type, "value": payload["value"], "timestamp": datetime.now()})
    st.experimental_rerun()

def start_mqtt():
    mqttc = mqtt.Client()
    mqttc.username_pw_set(HIVEMQ_USER, HIVEMQ_PASS)
    mqttc.connect(HIVEMQ_BROKER, HIVEMQ_PORT, 60)
    mqttc.on_message = on_message
    mqttc.subscribe(MQTT_TOPIC)
    mqttc.loop_start()

# Jalankan MQTT di thread
thread = threading.Thread(target=start_mqtt)
thread.start()

def show():
    # Judul dan navigasi
    st.title("Monitoring Page")
    st.button("Home", on_click=lambda: st.session_state.page("Homepage"))

    # Warna latar belakang menyerupai gambar
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #C3B1E1, #B0C4DE);
        }
        .temp-box {
            background-color: #f4a261;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            color: black;
            font-size: 24px;
            margin: 5px;
        }
        .temp-text {
            font-size: 14px;
            color: black;
        }
        .status-box {
            background-color: #f4a261;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            color: black;
            font-size: 24px;
            margin: 5px;
        }
        .status-text {
            font-size: 14px;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Bagian Kapasitas Tempat Sampah
    with st.container():
        st.markdown("<h3 style='text-align: center;'>Kapasitas Tempat Sampah (%)</h3>", unsafe_allow_html=True)
        kapasitas = st.session_state.sensor_data["kapasitas"]
        progress = st.progress(0)
        for i in range(int(kapasitas)):
            time.sleep(0.01)
            progress.progress((i + 1) / 100)
        st.write(f"**Terisi {kapasitas}%**")
        st.button("Reset Status", on_click=lambda: st.session_state.sensor_data.update({"kapasitas": 0}))

    # Kapasitas dengan Pie Chart
    st.subheader("Kapasitas Sampah (Pie Chart)")
    df = pd.DataFrame({
        "Kategori": ["Terisi", "Kosong"],
        "Nilai": [kapasitas, 100 - kapasitas]
    })
    pie_chart = alt.Chart(df).mark_arc().encode(
        theta="Nilai",
        color="Kategori"
    )
    st.altair_chart(pie_chart, use_container_width=True)

    # Bagian Suhu
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("🌡️ Suhu (°C)")
        with col2:
            suhu = st.session_state.sensor_data["suhu"]
            st.markdown(
                f"""
                <div class="temp-box">{suhu}°C</div>
                <div class="temp-text">Tiga puluh dua derajat</div>
                """,
                unsafe_allow_html=True
            )
        st.button("Alert", on_click=lambda: st.warning(f"Suhu {suhu}°C di atas batas normal!"))

    # Bagian Kelembapan
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("💧 Kelembapan (%)")
        with col2:
            kelembapan = st.session_state.sensor_data["kelembapan"]
            st.markdown(
                f"""
                <div class="temp-box">{kelembapan}%</div>
                <div class="temp-text">Tiga puluh dua derajat</div>
                """,
                unsafe_allow_html=True
            )
        st.button("Alert", on_click=lambda: st.warning(f"Kelembapan {kelembapan}% di atas batas normal!"))

    # Bagian Status Umum
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("⚠️ Status Umum (Aman / Hampir Penuh / Penuh)")
        with col2:
            status = "Aman" if kapasitas < 70 else "Hampir Penuh" if kapasitas < 90 else "Penuh"
            st.markdown(
                f"""
                <div class="status-box">{status}</div>
                <div class="status-text">Tempat sampah dalam keadaan {status.lower()}</div>
                """,
                unsafe_allow_html=True
            )

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 60px; font-style: italic; color: black;'>
        D4 Teknik Komputer A @SmartBin
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()