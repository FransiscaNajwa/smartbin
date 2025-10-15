import streamlit as st
import pymongo
import bcrypt
import paho.mqtt.client as mqtt
import json
import threading
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from streamlit_extras.metric_cards import style_metric_cards
import time

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://your-username:your-password@cluster0.mongodb.net/smartbin_db?retryWrites=true&w=majority")
db = client.smartbin_db
users = db.users
sensors = db.sensors
notifs = db.notifs

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

# CSS Kustom untuk desain
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #C3B1E1, #B0C4DE);
        font-family: 'Helvetica Neue', sans-serif;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 40px;
        background-color: #b3a6f2;
    }
    .header h2 {
        color: black;
        font-weight: bold;
    }
    .nav a {
        margin-left: 20px;
        text-decoration: none;
        color: black;
        font-weight: 500;
    }
    .btn {
        background-color: black;
        color: white;
        border-radius: 6px;
        padding: 6px 14px;
        text-decoration: none;
        font-weight: bold;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 25px;
        padding: 30px;
        margin: 20px;
    }
    .hero {
        text-align: center;
        padding: 40px;
    }
    .hero h1 {
        font-size: 40px;
        font-weight: 800;
    }
    .section-title {
        font-size: 28px;
        font-weight: bold;
        margin-top: 50px;
    }
    .center {
        text-align: center;
    }
    .how {
        font-style: italic;
        margin-top: 50px;
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-style: italic;
        color: black;
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
    .stContainer {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px auto;
        max-width: 400px;
    }
    .stSelectbox {
        background-color: #ffe6e6;
        border-radius: 10px;
    }
    .stButton {
        background-color: #ffe6e6;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header dengan waktu dinamis
st.markdown(f"""
<div class="header">
    <h2>SmartBin - {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}</h2>
    <div class="nav">
        <a class="btn" href="#" onClick='logout()'>Logout</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Logika logout dengan konfirmasi
def logout():
    if st.button("Yakin ingin logout?"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

# Semua fitur ditampilkan dalam tabs di landing page
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Welcome", "Login", "Register", "Dashboard", "Monitoring", "History", "Notifications"])

with tab1:
    st.markdown("""
    <div class="hero">
        <h1>Welcome to SmartBin</h1>
        <p>Tempat sampah pintar ini memanfaatkan sistem pemantauan berbasis IoT yang mampu mendeteksi kapasitas sampah serta kondisi lingkungan seperti suhu dan kelembapan. Data hasil pemantauan dikirim secara real-time ke aplikasi smartphone melalui jaringan WiFi.<br>
Pengguna akan menerima notifikasi ketika tempat sampah sudah hampir penuh atau penuh. Selain itu, pemantauan suhu dan kelembapan membantu menentukan kondisi lingkungan di dalam tempat sampah yang dapat menjadi indikator perlunya penggantian kantong sampah.<br>
Dengan sistem ini, pemilik rumah dapat segera mengambil tindakan sebelum sampah meluber, sekaligus mendorong kebiasaan pengelolaan sampah yang lebih higienis dan efektif.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Fitur SmartBin")
    st.markdown("""
    - **Dashboard**: Rekap real-time dari monitoring, chart riwayat, notifikasi, dan log teks.
    - **Monitoring**: Lihat kapasitas sampah (pie chart), suhu, dan kelembapan dari IoT via MQTT dan MongoDB.
    - **History**: Filter waktu, rata-rata 7 hari untuk kapasitas/suhu/kelembapan, tabel riwayat, log.
    - **Notifications**: Section untuk kapasitas sampah dan suhu/kelembapan.
    """)

with tab2:
    st.title("Login")

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
                st.experimental_rerun()
            else:
                st.error("Username/email/password salah!")

    st.markdown("<p>Tidak punya akun? Pilih tab Register</p>", unsafe_allow_html=True)

with tab3:
    st.title("Register")

    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Konfirmasi Password", type="password")
        submitted = st.form_submit_button("Submit")

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
                    st.experimental_rerun()

    st.markdown("<p>Sudah punya akun? Pilih tab Login</p>", unsafe_allow_html=True)

with tab4:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://cdn.pixabay.com/photo/2017/09/06/19/05/garbage-2729601_1280.jpg", use_column_width=True)
    with col2:
        st.markdown("<div class='hero-text'><h1>Welcome to SmartBin</h1></div>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🗑️ Kapasitas Sampah")
    st.caption("Persentase tempat sampah terisi")

    latest_data = sensors.find_one(sort=[("timestamp", -1)]) if sensors.count_documents({}) > 0 else {"kapasitas": 65}
    progress = st.progress(0)
    for i in range(int(latest_data["kapasitas"])):
        time.sleep(0.01)
        progress.progress(i + 1)
    st.write(f"**Terisi {latest_data['kapasitas']}%**")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 🌡️ Suhu")
        st.caption("Monitoring kondisi dalam tempat sampah")
        st.metric(label="", value=f"{latest_data.get('suhu', 32)}°C")
    with col4:
        st.markdown("### 💧 Kelembapan")
        st.caption("Menilai kondisi lingkungan")
        st.metric(label="", value=f"{latest_data.get('kelembapan', 32)}%")

    style_metric_cards(border_left_color="#A57AFF", border_color="#E3D7FF")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='chart-section'>
    <h3>📈 Chart Section</h3>
    <i>Kapasitas tempat sampah, suhu, dan kelembapan</i><br>
    <i>Pilihan filter waktu: “Hari ini | Minggu ini | Bulan ini”</i>
    </div>
    """, unsafe_allow_html=True)

    data = list(sensors.find().sort("timestamp", -1).limit(5)) if sensors.count_documents({}) > 0 else [
        {"kapasitas": 60, "suhu": 31, "kelembapan": 55},
        {"kapasitas": 65, "suhu": 32, "kelembapan": 58},
        {"kapasitas": 70, "suhu": 33, "kelembapan": 60},
        {"kapasitas": 75, "suhu": 33, "kelembapan": 63},
        {"kapasitas": 80, "suhu": 32, "kelembapan": 61}
    ]
    chart_data = {k: [d.get(k, 0) for d in data] for k in ["kapasitas", "suhu", "kelembapan"]}
    st.line_chart(chart_data)

    st.markdown("""
    <div class='history-section'>
    <h3>🧾 Riwayat Aktivitas</h3>
    <b>📅 07/10/2025</b><br>
    [10:20] Tempat sampah penuh<br>
    [08:45] Kantong diganti<br>
    [Kemarin] Suhu di atas batas normal
    </div>
    """, unsafe_allow_html=True)

with tab5:
    st.title("Monitoring Page")

    with st.container():
        st.markdown("<h3 style='text-align: center;'>Kapasitas Tempat Sampah (%)</h3>", unsafe_allow_html=True)
        kapasitas = st.session_state.sensor_data["kapasitas"]
        progress = st.progress(0)
        for i in range(int(kapasitas)):
            time.sleep(0.01)
            progress.progress((i + 1) / 100)
        st.write(f"**Terisi {kapasitas}%**")
        st.button("Reset Status", on_click=lambda: st.session_state.sensor_data.update({"kapasitas": 0}))

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

with tab6:
    st.title("History Page")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        rentang = st.selectbox("Rentang Waktu", ["7 Hari Terakhir", "Custom"])
    with col2:
        start_date = st.date_input("Tanggal Mulai", datetime.now() - timedelta(days=7))
    with col3:
        end_date = st.date_input("Tanggal Akhir", datetime.now())

    if st.button("Filter"):
        query = {"timestamp": {"$gte": start_date, "$lte": end_date}}
        data = list(sensors.find(query).sort("timestamp", -1))

        if data:
            df = pd.DataFrame(data)

            st.markdown("<h3 style='text-align: center;'>Rata-rata Kapasitas Sampah per Hari</h3>", unsafe_allow_html=True)
            kapasitas_avg = df.groupby(df['timestamp'].dt.date)['kapasitas'].mean()
            st.bar_chart(kapasitas_avg)

            st.markdown("<h3 style='text-align: center;'>Rata-rata Suhu & Kelembapan</h3>", unsafe_allow_html=True)
            suhu_avg = df['suhu'].mean()
            kelembapan_avg = df['kelembapan'].mean()
            col1, col2 = st.columns(2)
            col1.metric("Suhu Rata-rata", f"{suhu_avg:.1f}°C")
            col2.metric("Kelembapan Rata-rata", f"{kelembapan_avg:.1f}%")

            st.markdown("<h3 style='text-align: center;'>Tabel Riwayat</h3>", unsafe_allow_html=True)
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write("⏰ Waktu")
                with col2:
                    st.write("🗑️ Kapasitas (%)")
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write("🌡️ Suhu (°C)")
                with col2:
                    st.write("💧 Kelembapan (%)")
            st.dataframe(df[['timestamp', 'kapasitas', 'suhu', 'kelembapan']])

            st.markdown("<h3 style='text-align: center;'>Log</h3>", unsafe_allow_html=True)
            for entry in data:
                st.write(f"[{entry['timestamp'].strftime('%H:%M')}] {entry['type']}: {entry['value']}")
        else:
            st.info("Tidak ada data untuk rentang waktu ini.")

with tab7:
    st.title("Notifications Page")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("🔔")
    with col2:
        if st.button("Clear"):
            notifs.delete_many({})
            st.experimental_rerun()

    selected_category = st.selectbox("Semua", ["Semua", "Kapasitas Sampah", "Suhu & Kelembapan"], index=0)

    if selected_category in ["Semua", "Kapasitas Sampah"]:
        with st.container():
            st.markdown("<h3 style='text-align: center; background-color: #ff9999; padding: 10px; border-radius: 10px;'>🔔 Kategori: Kapasitas Sampah</h3>", unsafe_allow_html=True)
            kapasitas_notifs = list(notifs.find({"category": "kapasitas"}).sort("timestamp", -1))
            if kapasitas_notifs:
                for n in kapasitas_notifs:
                    st.write(f"[{n['timestamp'].strftime('%d %b %Y, %H:%M WIB')}] {n['message']}")
            else:
                st.write("Tidak ada notifikasi untuk kategori ini.")

    if selected_category in ["Semua", "Suhu & Kelembapan"]:
        with st.container():
            st.markdown("<h3 style='text-align: center; background-color: #ff9999; padding: 10px; border-radius: 10px;'>🔔 Kategori: Suhu & Kelembapan</h3>", unsafe_allow_html=True)
            lingkungan_notifs = list(notifs.find({"category": "lingkungan"}).sort("timestamp", -1))
            if lingkungan_notifs:
                for n in lingkungan_notifs:
                    st.write(f"[{n['timestamp'].strftime('%d %b %Y, %H:%M WIB')}] {n['message']}")
            else:
                st.write("Tidak ada notifikasi untuk kategori ini.")

# Footer
st.markdown("""
<div class="footer">
    D4 Teknik Komputer A @SmartBin
</div>
""", unsafe_allow_html=True)