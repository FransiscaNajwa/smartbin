import streamlit as st
from streamlit_app.utils.ui_helper import load_css
from PIL import Image
from pathlib import Path

def show_home_page(go_to):
    load_css("style.css")

    # Tombol navigasi
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
    with nav_col1:
        if st.button("Monitoring"):
            go_to("MonitoringPage")
    with nav_col2:
        if st.button("Riwayat"):
            go_to("RiwayatPage")
    with nav_col3:
        if st.button("Profile"):
            go_to("ProfilePage")
    with nav_col4:
        if st.button("Notifikasi"):
            go_to("NotifikasiPage")
    with nav_col5:
        if st.button("Logout"):
            go_to("LoginPage")

    # Welcome Section
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to SmartBin</h1>
            <h3>Track, Monitor, Stay Clean</h3>
        </div>
    """, unsafe_allow_html=True)

    # Gambar SmartBin di tengah
    st.markdown("<div class='welcome-section' style='text-align:center;'>", unsafe_allow_html=True)
    img_path = Path(__file__).resolve().parent.parent / "streamlit_app/assets/sampah.png"
    try:
        image = Image.open(img_path)
        st.image(image, width=300)
    except FileNotFoundError:
        st.warning("⚠️ Gambar 'sampah.png' tidak ditemukan.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Monitoring Preview
    st.markdown("<div class='section-title'>Monitoring Page</div>", unsafe_allow_html=True)
    st.markdown("🗑️ **Kapasitas Tempat Sampah (%)**")
    st.markdown("<div class='info-card'>68%</div>", unsafe_allow_html=True)
    st.markdown("🌡️ **Suhu (°C)**")
    st.markdown("<div class='info-card'>32°C</div>", unsafe_allow_html=True)
    st.markdown("💧 **Kelembapan (%)**")
    st.markdown("<div class='info-card'>60%</div>", unsafe_allow_html=True)

    # Riwayat Preview dengan Filter
    st.markdown("<div class='section-title'>Riwayat Page</div>", unsafe_allow_html=True)
    filter_option = st.radio("Filter berdasarkan:", ["Hari", "Minggu", "Bulan"], horizontal=True)

    if filter_option == "Hari":
        selected_date = st.date_input("Pilih tanggal")
        st.markdown(f"#### Riwayat untuk tanggal: {selected_date.strftime('%d/%m/%Y')}")
        data = {
            "🕓 Waktu": ["08:00", "10:30", "13:00"],
            "🗑️ Kapasitas (%)": [60, 68, 72],
            "🌡️ Suhu (°C)": [30, 32, 33],
            "💧 Kelembapan (%)": [55, 60, 62]
        }
        st.table(data)

    elif filter_option == "Minggu":
        selected_week = st.number_input("Pilih minggu ke-", min_value=1, max_value=52, step=1)
        st.markdown(f"#### Riwayat untuk minggu ke-{selected_week}")
        data = {
            "🕓 Hari": ["Senin", "Rabu", "Jumat"],
            "🗑️ Kapasitas (%)": [58, 65, 70],
            "🌡️ Suhu (°C)": [29, 31, 32],
            "💧 Kelembapan (%)": [54, 57, 60]
        }
        st.table(data)

    elif filter_option == "Bulan":
        bulan_dict = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
            "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
            "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }
        selected_month = st.selectbox("Pilih bulan", list(bulan_dict.keys()))
        st.markdown(f"#### Riwayat untuk bulan: {selected_month}")
        data = {
            "🕓 Tanggal": [f"01/{bulan_dict[selected_month]}", f"15/{bulan_dict[selected_month]}", f"28/{bulan_dict[selected_month]}"],
            "🗑️ Kapasitas (%)": [55, 67, 72],
            "🌡️ Suhu (°C)": [28, 30, 32],
            "💧 Kelembapan (%)": [52, 56, 59]
        }
        st.table(data)

    # Footer
    st.markdown("<div class='footer'>3 D4 Teknik Komputer A @SmartBin</div>", unsafe_allow_html=True)