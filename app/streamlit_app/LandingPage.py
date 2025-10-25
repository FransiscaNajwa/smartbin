import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit_app.utils.ui_helper import load_css
import base64
from io import BytesIO

def show_landing_page(go_to):
    load_css("style.css")

    # Welcome Section
    st.markdown("""
        <div class='landing-header'>
            <h2>Welcome to SmartBin</h2>
            <h4>Track, Monitor, and Stay Clean...</h4>
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
    st.table({
        "🕓 Waktu": ["10:30", "10:45"],
        "🗑️ Kapasitas (%)": [65, 68],
        "🌡️ Suhu (°C)": [31, 32],
        "💧 Kelembapan (%)": [58, 60]
    })

    # How it works
    st.markdown("<div class='section-title'>How it works?</div>", unsafe_allow_html=True)
    st.markdown("""
    **1. Hubungkan Perangkat IoT**  
    Sambungkan sensor dengan WiFi dan sistem SmartBin  

    **2. Pantau dari Website**  
    Login dan lihat status tempat sampah secara real-time  

    **3. Dapatkan Notifikasi**  
    Terima peringatan ketika tempat sampah penuh dan suhu dalam tempat sampah meningkat
    """)

    # Tombol Login dan Register di bawah poin 3
    st.markdown("---")
    if st.button("Login"):
        go_to("LoginPage")
    if st.button("Register"):
        go_to("RegisterPage")

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