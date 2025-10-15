import streamlit as st
import pymongo
import paho.mqtt.client as mqtt
import json
import threading
import bcrypt
from datetime import datetime

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://smartbinuser:<SmartBin123>@cluster0.inq2nbd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.smartbin_db
users = db.users
sensors = db.sensors

# MQTT Konfigurasi (HiveMQ)
HIVEMQ_BROKER = "your-hivemq-broker.com"
HIVEMQ_PORT = 1883
HIVEMQ_USER = "user"
HIVEMQ_PASS = "pass"
MQTT_TOPIC = "smartbin/sensor/#"

# State untuk data real-time dan login
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {"kapasitas": 0, "suhu": 0, "kelembapan": 0}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_register" not in st.session_state:
    st.session_state.show_register = False

# MQTT Callback
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic_parts = msg.topic.split("/")
    if len(topic_parts) > 2:
        sensor_type = topic_parts[2]
        st.session_state.sensor_data[sensor_type] = payload["value"]
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

# Konfigurasi halaman utama
st.set_page_config(page_title="SmartBin", page_icon="🗑️", layout="wide")

# CSS Kustom untuk desain mockup
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #C3B1E1, #B0C4DE);
        font-family: 'Helvetica Neue', sans-serif;
        color: #2c3e50;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 40px;
        background-color: #6B48FF;
        border-bottom: 2px solid #4A2DFF;
    }
    .header h2 {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 24px;
        margin: 0;
    }
    .nav a {
        margin-left: 20px;
        text-decoration: none;
        color: #FFFFFF;
        font-weight: 500;
    }
    .btn {
        background-color: #6B48FF;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 6px 14px;
        text-decoration: none;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .btn:hover {
        background-color: #4A2DFF;
    }
    .hero {
        text-align: center;
        padding: 40px;
        background-color: #FFFFFF;
        border-radius: 15px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .hero h1 {
        font-size: 36px;
        font-weight: 800;
        color: #2c3e50;
    }
    .hero p {
        font-size: 18px;
        color: #7f8c8d;
        margin-top: 10px;
    }
    .feature-section {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
    }
    .feature-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        width: 28%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: scale(1.05);
    }
    .feature-card h3 {
        font-size: 18px;
        font-weight: 700;
        color: #2c3e50;
    }
    .feature-card p {
        font-size: 14px;
        color: #7f8c8d;
    }
    .chart-section {
        text-align: center;
        margin: 30px 0;
    }
    .chart-section h3 {
        font-size: 24px;
        font-weight: 700;
        color: #2c3e50;
    }
    .how-section {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 20px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .how-section h3 {
        font-size: 22px;
        font-weight: 700;
        color: #2c3e50;
        font-style: italic;
    }
    .how-section b {
        font-size: 16px;
        color: #2c3e50;
    }
    .how-section p {
        font-size: 14px;
        color: #7f8c8d;
    }
    .action-buttons {
        text-align: center;
        margin: 20px 0;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        background-color: #6B48FF;
        color: #FFFFFF;
        border-top: 2px solid #4A2DFF;
        font-size: 14px;
    }
    .login-form, .register-form {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 400px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        display: none;
    }
    .login-form.active, .register-form.active {
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="header">
    <h2>SmartBin - {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}</h2>
    <div class="nav">
        <a class="btn" href="#" onClick='show_login_form()'>Login</a>
        <a class="btn" href="#" onClick='show_register_form()'>Register</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>Welcome to SmartBin</h1>
    <p>Track, Monitor, Stay Clean with Smart Technology...</p>
</div>
""", unsafe_allow_html=True)

# Gambar Utama
st.image("https://cdn.pixabay.com/photo/2017/09/06/19/05/garbage-2729601_1280.jpg", use_column_width=True)

# Section Fitur (dengan tombol/card interaktif)
st.markdown("""
<div class="feature-section">
    <div class="feature-card" onClick='go_to_monitoring()'>
        <img src="https://www.shutterstock.com/shutterstock/photos/174287021/display_1500/stock-vector-trash-can-with-garbage-and-recycling-symbol-174287021.jpg" width="100%">
        <h3>Monitoring Real-Time</h3>
        <p>Pantau kapasitas, suhu, dan kelembapan secara langsung</p>
    </div>
    <div class="feature-card" onClick='go_to_notifications()'>
        <img src="https://www.shutterstock.com/shutterstock/photos/174287021/display_1500/stock-vector-trash-can-with-garbage-and-recycling-symbol-174287021.jpg" width="100%">
        <h3>Notifikasi Otomatis</h3>
        <p>Dapatkan peringatan saat tempat sampah hampir penuh</p>
    </div>
    <div class="feature-card" onClick='go_to_history()'>
        <img src="https://www.shutterstock.com/shutterstock/photos/174287021/display_1500/stock-vector-trash-can-with-garbage-and-recycling-symbol-174287021.jpg" width="100%">
        <h3>Riwayat & Grafik</h3>
        <p>Analisis tren kebersihan harian dan bulanan</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Section Grafik Data Riwayat (Mockup)
st.markdown("<div class='chart-section'>", unsafe_allow_html=True)
st.subheader("Grafik Data Riwayat")
st.image("https://cdn.theguardian.com/environment/2020/mar/18/recycling-data.jpg", use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Section How it works?
st.markdown("""
<div class="how-section">
    <h3>How it works?</h3>
    <b>1. Hubungkan Perangkat IoT</b><br>
    Pasang sensor dan sambungkan ke WiFi<br><br>
    <b>2. Pantau dari Platform</b><br>
    Login untuk melihat status real-time<br><br>
    <b>3. Terima Notifikasi</b><br>
    Dapatkan pemberitahuan saat dibutuhkan<br><br>
    <p>Bersama kita wujudkan lingkungan yang bersih! 🌱</p>
</div>
""", unsafe_allow_html=True)

# Action Buttons
st.markdown("""
<div class="action-buttons">
    <a class="btn" href="#" onClick='show_login_form()'>Login</a>
    <a class="btn" href="#" onClick='show_register_form()'>Register</a>
</div>
""", unsafe_allow_html=True)

# Form Login (ditampilkan jika tombol Login ditekan)
st.markdown("""
<div class="login-form" id="login-form">
    <h3>Login</h3>
""", unsafe_allow_html=True)
if st.session_state.show_login:
    with st.form("login_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            user = users.find_one({"username": username, "email": email})
            if user and bcrypt.checkpw(password.encode(), user["password"]):
                st.success("Login berhasil!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.show_login = False
                st.experimental_rerun()
            else:
                st.error("Username/email/password salah!")
st.markdown("</div>", unsafe_allow_html=True)

# Form Register (ditampilkan jika tombol Register ditekan)
st.markdown("""
<div class="register-form" id="register-form">
    <h3>Register</h3>
""", unsafe_allow_html=True)
if st.session_state.show_register:
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Konfirmasi Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if not all([username, email, password, confirm_password]):
                st.error("Harap isi semua kolom!")
            elif password != confirm_password:
                st.error("Password tidak cocok!")
            else:
                if users.find_one({"username": username}):
                    st.error("Username sudah terdaftar!")
                else:
                    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                    users.insert_one({"username": username, "email": email, "password": hashed_pw, "name": username})
                    st.success("Pendaftaran berhasil!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.show_register = False
                    st.experimental_rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Demo Data Sensor (Real-Time)
if st.session_state.logged_in:
    st.subheader("Data Sensor Terkini")
    st.write(f"Kapasitas: {st.session_state.sensor_data['kapasitas']}%")
    st.write(f"Suhu: {st.session_state.sensor_data['suhu']}°C")
    st.write(f"Kelembapan: {st.session_state.sensor_data['kelembapan']}%")

# Footer
st.markdown("""
<div class="footer">
    D4 Teknik Komputer A @SmartBin - © 2025
</div>
""", unsafe_allow_html=True)

# Fungsi JavaScript untuk navigasi (mockup, akan diganti dengan logika nyata)
st.markdown("""
<script>
function go_to_monitoring() {
    alert("Navigasi ke Monitoring (akan diimplementasikan)");
}
function go_to_notifications() {
    alert("Navigasi ke Notifications (akan diimplementasikan)");
}
function go_to_history() {
    alert("Navigasi ke History (akan diimplementasikan)");
}
function show_login_form() {
    document.getElementById('login-form').classList.add('active');
    document.getElementById('register-form').classList.remove('active');
}
function show_register_form() {
    document.getElementById('register-form').classList.add('active');
    document.getElementById('login-form').classList.remove('active');
}
</script>
""", unsafe_allow_html=True)