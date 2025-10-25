import streamlit as st
from streamlit_app.utils.ui_helper import load_css
from PIL import Image
from pathlib import Path
from io import BytesIO
import base64

def show_home_page(go_to):
    load_css("style.css")

    # Welcome Section
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to SmartBin</h1>
            <h3>Track, Monitor, Stay Clean</h3>
        </div>
    """, unsafe_allow_html=True)

    # Gambar SmartBin responsif di tengah
    img_path = Path(__file__).resolve().parent.parent / "streamlit_app/assets/sampah.png"
    try:
        image = Image.open(img_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        st.markdown(f"""
            <div class='welcome-section'>
                <img src="data:image/png;base64,{img_base64}" class="responsive-img">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Gambar 'sampah.png' tidak ditemukan.")

    # Monitoring Preview
    st.markdown("<div class='section-title'>Monitoring Page</div>", unsafe_allow_html=True)
    st.markdown("🗑️ **Kapasitas Tempat Sampah (%)**")
    st.markdown("<div class='info-card'>68%</div>", unsafe_allow_html=True)
    st.markdown("🌡️ **Suhu (°C)**")
    st.markdown("<div class='info-card'>32°C</div>", unsafe_allow_html=True)
    st.markdown("💧 **Kelembapan (%)**")
    st.markdown("<div class='info-card'>60%</div>", unsafe_allow_html=True)

    # Riwayat Preview
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

    # Navigasi di bagian bawah (berjajar ke bawah)
    st.markdown("---")
    if st.button("Profile"):
        go_to("ProfilePage")
    if st.button("Notifikasi"):
        go_to("NotifikasiPage")
    if st.button("Logout"):
        go_to("LandingPage")

   # Footer
    st.markdown("""
    <div class='italic'>
        <b>Bersama kita wujudkan kebersihan berkelanjutan</b><br>
        <b>Mulai langkah kecil untuk bumi yang lebih hijau</b>
    </div>
    <div class='footer'>
        <b>3 D4 Teknik Komputer A</b><br>
        <b>@SmartBin</b>
    </div>
    """, unsafe_allow_html=True)