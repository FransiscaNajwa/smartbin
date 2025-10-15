import streamlit as st
import pymongo
import bcrypt
import time
from streamlit_extras.metric_cards import style_metric_cards

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/smartbin_db")
db = client.smartbin_db
users = db.users
sensors = db.sensors  # Collection untuk data sensor (opsional, tambahkan jika ada)

def show():
    # Konfigurasi halaman
    st.set_page_config(page_title="SmartBin Dashboard", page_icon="🗑️", layout="wide")

    # ======== CSS Kustom ========
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #C3B1E1, #B0C4DE);
            font-family: 'Poppins', sans-serif;
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
        .btn-logout {
            background-color: black;
            color: white;
            border-radius: 6px;
            padding: 6px 14px;
            text-decoration: none;
            font-weight: bold;
        }
        .hero {
            display: flex;
            align-items: center;
            justify-content: space-around;
            padding: 30px;
        }
        .hero-text {
            text-align: center;
        }
        .hero-text h1 {
            font-size: 36px;
            font-weight: 800;
            color: #222;
        }
        .section {
            background-color: #f9f9f9;
            border-radius: 25px;
            padding: 30px;
            margin: 40px 60px;
        }
        .chart-section, .history-section {
            margin: 40px 60px;
        }
        .footer {
            text-align: center;
            margin-top: 60px;
            font-style: italic;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    # ======== HEADER ========
    st.markdown("""
    <div class="header">
        <h2>SmartBin</h2>
        <div class="nav">
            <a href="#" onClick='change_page("Monitoring")'>Monitoring</a>
            <a href="#" onClick='change_page("Riwayat")'>Riwayat</a>
            <a href="#" onClick='change_page("Profil")'>Profil</a>
            <a class="btn-logout" href="#" onClick='change_page("Login")'>Logout</a> <!-- Logout ke Login -->
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ======== HERO SECTION ========
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://cdn.pixabay.com/photo/2017/09/06/19/05/garbage-2729601_1280.jpg", use_column_width=True)
    with col2:
        st.markdown("<div class='hero-text'><h1>Welcome to SmartBin</h1></div>", unsafe_allow_html=True)

    # ======== STATUS MONITORING ========
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🗑️ Kapasitas Sampah")
    st.caption("Persentase tempat sampah terisi")

    # Ambil data terakhir dari MongoDB (simulasi jika belum ada data real-time)
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

    # ======== CHART SECTION ========
    st.markdown("""
    <div class='chart-section'>
    <h3>📈 Chart Section</h3>
    <i>Kapasitas tempat sampah, suhu, dan kelembapan</i><br>
    <i>Pilihan filter waktu: “Hari ini | Minggu ini | Bulan ini”</i>
    </div>
    """, unsafe_allow_html=True)

    # Ambil data dari MongoDB (simulasi jika belum ada data real-time)
    data = list(sensors.find().sort("timestamp", -1).limit(5)) if sensors.count_documents({}) > 0 else [
        {"kapasitas": 60, "suhu": 31, "kelembapan": 55},
        {"kapasitas": 65, "suhu": 32, "kelembapan": 58},
        {"kapasitas": 70, "suhu": 33, "kelembapan": 60},
        {"kapasitas": 75, "suhu": 33, "kelembapan": 63},
        {"kapasitas": 80, "suhu": 32, "kelembapan": 61}
    ]
    chart_data = {k: [d.get(k, 0) for d in data] for k in ["kapasitas", "suhu", "kelembapan"]}
    chart_placeholder = st.empty()
    chart_placeholder.line_chart(chart_data)

    # ======== RIWAYAT ========
    st.markdown("""
    <div class='history-section'>
    <h3>🧾 Riwayat Aktivitas</h3>
    <b>📅 07/10/2025</b><br>
    [10:20] Tempat sampah penuh<br>
    [08:45] Kantong diganti<br>
    [Kemarin] Suhu di atas batas normal
    </div>
    """, unsafe_allow_html=True)

    # ======== FOOTER ========
    st.markdown("""
    <div class='footer'>
    3 D4 Teknik Komputer A<br>
    @SmartBin
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()