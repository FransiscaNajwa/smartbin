import streamlit as st
from streamlit_app.utils.ui_helper import load_css
from PIL import Image
from pathlib import Path

def show_home_page(go_to):
    load_css("style.css")

    # Header Navigasi
    st.markdown("""
    <div class="nav-bar">
        <div class="logo">SmartBin</div>
        <div class="nav-buttons">
            <button onclick="window.location.href='MonitoringPage'">Monitoring</button>
            <button onclick="window.location.href='RiwayatPage'">Riwayat</button>
            <button onclick="window.location.href='ProfilePage'">Profile</button>
            <button onclick="window.location.href='Logout'">Logout</button>
            <span class="bell-icon">🔔</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome Section
    st.markdown("<div class='welcome-section'>", unsafe_allow_html=True)
    img_path = Path(__file__).resolve().parent.parent / "assets" / "smartbin.png"
    try:
        image = Image.open(img_path)
        st.image(image, width=300)
    except FileNotFoundError:
        st.warning("⚠️ Gambar 'smartbin.png' tidak ditemukan.")
    st.markdown("<h1>Welcome to SmartBin</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Monitoring Section
    st.markdown("<div class='monitoring-section'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='metric-card'>
        <h3>🗑️ Kapasitas Sampah</h3>
        <p>Persentase tempat sampah terisi</p>
        <div class='progress-circle'>68%</div>
    </div>
    <div class='metric-card'>
        <h3>🌡️ Suhu</h3>
        <p>Monitoring kondisi dalam tempat sampah</p>
        <div class='metric-value'>32°C</div>
    </div>
    <div class='metric-card'>
        <h3>💧 Kelembapan</h3>
        <p>Menilai kondisi lingkungan</p>
        <div class='metric-value'>32°C</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Chart Section
    st.markdown("<div class='chart-section'>", unsafe_allow_html=True)
    st.markdown("### ✅ Chart Section")
    st.markdown("Kapasitas tempat sampah, suhu, dan kelembapan")
    st.markdown("Pilihan filter waktu: **Hari ini | Minggu ini | Bulan ini**")
    st.empty()  # Placeholder chart
    st.markdown("</div>", unsafe_allow_html=True)

    # Riwayat Aktivitas
    st.markdown("<div class='history-section'>", unsafe_allow_html=True)
    st.markdown("### 📋 Riwayat Aktivitas")
    st.markdown("""
    - [🗓️ 07/10/2025 10:20] Tempat sampah penuh
    - [🕒 08:45] Kantong diganti
    - [📛 Kemarin] Suhu di atas batas normal
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>3 D4 Teknik Komputer A @SmartBin</div>", unsafe_allow_html=True)

    # Logout Button
    if st.button("Logout"):
        go_to("LoginPage")