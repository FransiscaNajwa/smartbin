import streamlit as st
import pymongo
import paho.mqtt.client as mqtt
import json
import threading
import altair as alt
import pandas as pd
from datetime import datetime, timedelta
import time

# # Koneksi MongoDB (ganti dengan connection string Anda dari MongoDB Atlas)
# try:
#     client = pymongo.MongoClient(
#         "mongodb+srv://<your-username>:<your-password>@cluster0.inq2nbd.mongodb.net/smartbin_db?retryWrites=true&w=majority&appName=Cluster0"
#     )
#     db = client.smartbin_db
#     sensors = db.sensors  # Collection untuk data sensor
# except pymongo.errors.ConfigurationError as e:
#     st.error(f"Kesalahan koneksi MongoDB: {e}. Periksa connection string dan whitelist IP di MongoDB Atlas.")
#     st.stop()

# # MQTT Konfigurasi
# HIVEMQ_BROKER = "your-hivemq-broker.com"
# HIVEMQ_PORT = 1883
# HIVEMQ_USER = "user"
# HIVEMQ_PASS = "pass"
# MQTT_TOPIC = "smartbin/sensor/#"

# State untuk data real-time dan login
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {"kapasitas": 0, "suhu": 0, "kelembapan": 0, "status": "Normal"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# MQTT Callback
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic_parts = msg.topic.split("/")
    if len(topic_parts) > 2:
        sensor_type = topic_parts[2]
        if sensor_type == "status":
            st.session_state.sensor_data[sensor_type] = payload.get("value", "Normal")
        else:
            st.session_state.sensor_data[sensor_type] = payload.get("value", 0)
        sensors.insert_one({
            "type": sensor_type,
            "value": payload.get("value", 0 if sensor_type != "status" else "Normal"),
            "timestamp": datetime.now()
        })
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

# Konfigurasi halaman utama
st.set_page_config(page_title="SmartBin Monitoring", page_icon="🗑️", layout="wide")

# CSS Kustom berdasarkan desain yang didiskusikan
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #E0E7FF, #D1E8FF);
        font-family: 'Poppins', sans-serif;
        color: #2C3E50;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 40px;
        background-color: #4A90E2; /* Warna biru muda untuk header */
        border-bottom: 3px solid #357ABD;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .header h2 {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 24px;
        margin: 0;
    }
    .nav-buttons a, .nav-buttons button {
        margin-left: 15px;
        text-decoration: none;
        color: #FFFFFF;
        font-weight: 500;
        background-color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        cursor: pointer;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .nav-buttons a:hover, .nav-buttons button:hover {
        background-color: #357ABD;
        color: #FFFFFF;
    }
    .btn-logout {
        background-color: #FFFFFF;
        color: #4A90E2;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        text-decoration: none;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .btn-logout:hover {
        background-color: #D3D3D3;
        color: #2C3E50;
    }
    .hero {
        text-align: center;
        padding: 30px;
        background-color: #FFFFFF;
        border-radius: 15px;
        margin: 20px auto;
        max-width: 900px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .hero-text h1 {
        font-size: 36px;
        font-weight: 800;
        color: #2C3E50;
    }
    .section {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 40px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .monitoring-box {
        background-color: #F0F4F8;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .chart-section, .history-section {
        margin: 20px 40px;
    }
    .footer {
        text-align: center;
        padding: 10px;
        background-color: #4A90E2;
        color: #FFFFFF;
        border-top: 2px solid #357ABD;
        font-size: 14px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header dengan tombol Home dan Alert
st.markdown(f"""
<div class="header">
    <h2>Monitoring Page - {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}</h2>
    <div class="nav-buttons">
        <a href="#" onClick='change_page("Home")'>Home</a>
        <button onClick='show_alert()'>Alert</button>
        <a class="btn-logout" href="#" onClick='change_page("Login")'>Logout</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class='hero'>
    <div class='hero-text'>
        <h1>SmartBin Monitoring</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# Monitoring Section dalam satu box
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🗑️ Status Monitoring")

# Ambil data terakhir dari MongoDB atau state
latest_data = sensors.find_one(sort=[("timestamp", -1)]) if sensors.count_documents({}) > 0 else st.session_state.sensor_data
progress = st.progress(0)
for i in range(int(latest_data["kapasitas"])):
    time.sleep(0.01)
    progress.progress(i + 1)

st.markdown("<div class='monitoring-box'>", unsafe_allow_html=True)
st.write(f"**Kapasitas:** {latest_data['kapasitas']}%")
st.write(f"**Suhu:** {latest_data['suhu']}°C")
st.write(f"**Kelembapan:** {latest_data['kelembapan']}%")
st.write(f"**Status:** {latest_data['status']}")
st.markdown("</div>", unsafe_allow_html=True)

# Pie Chart untuk Kapasitas
st.subheader("📊 Kapasitas Tempat Sampah")
pie_data = pd.DataFrame({
    "Kategori": ["Terisi", "Kosong"],
    "Persentase": [latest_data["kapasitas"], 100 - latest_data["kapasitas"]]
})
pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta=alt.Theta(field="Persentase", type="quantitative"),
    color=alt.Color(field="Kategori", type="nominal", legend=None),
    tooltip=["Kategori", "Persentase"]
).properties(
    width=300,
    height=300
)
st.altair_chart(pie_chart, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Chart Section (Tren Suhu dan Kelembapan)
st.markdown("<div class='chart-section'>", unsafe_allow_html=True)
st.subheader("📈 Tren Data Sensor")
st.caption("Suhu dan Kelembapan")

data = list(sensors.find({"type": {"$in": ["suhu", "kelembapan"]}}).sort("timestamp", -1).limit(10)) if sensors.count_documents({}) > 0 else [
    {"type": "suhu", "value": 31, "timestamp": datetime.now() - timedelta(minutes=50)},
    {"type": "suhu", "value": 32, "timestamp": datetime.now() - timedelta(minutes=40)},
    {"type": "suhu", "value": 33, "timestamp": datetime.now() - timedelta(minutes=30)},
    {"type": "suhu", "value": 33, "timestamp": datetime.now() - timedelta(minutes=20)},
    {"type": "suhu", "value": 32, "timestamp": datetime.now() - timedelta(minutes=10)},
    {"type": "suhu", "value": 34, "timestamp": datetime.now()},
    {"type": "kelembapan", "value": 55, "timestamp": datetime.now() - timedelta(minutes=50)},
    {"type": "kelembapan", "value": 58, "timestamp": datetime.now() - timedelta(minutes=40)},
    {"type": "kelembapan", "value": 60, "timestamp": datetime.now() - timedelta(minutes=30)},
    {"type": "kelembapan", "value": 63, "timestamp": datetime.now() - timedelta(minutes=20)},
    {"type": "kelembapan", "value": 61, "timestamp": datetime.now() - timedelta(minutes=10)},
    {"type": "kelembapan", "value": 65, "timestamp": datetime.now()}
]
df = pd.DataFrame(data)
chart = alt.Chart(df).mark_line().encode(
    x=alt.X('timestamp:T', title='Waktu'),
    y=alt.Y('value:Q', title='Nilai'),
    color='type:N',
    tooltip=['timestamp', 'type', 'value']
).properties(
    width=800,
    height=300
).interactive()
st.altair_chart(chart, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# History Section
st.markdown("<div class='history-section'>", unsafe_allow_html=True)
st.subheader("🧾 Riwayat Aktivitas")
st.write(f"<b>📅 {datetime.now().strftime('%d/%m/%Y')}</b>", unsafe_allow_html=True)
st.write("[10:20] Tempat sampah penuh")
st.write("[08:45] Kantong diganti")
st.write("[Kemarin] Suhu di atas batas normal")
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    3 D4 Teknik Komputer A @SmartBin
</div>
""", unsafe_allow_html=True)

# JavaScript untuk navigasi dan alert
st.markdown("""
<script>
function change_page(page) {
    alert("Navigasi ke " + page + " (akan diimplementasikan)");
}
function show_alert() {
    alert("Alert: Periksa status tempat sampah!");
}
</script>
""", unsafe_allow_html=True)