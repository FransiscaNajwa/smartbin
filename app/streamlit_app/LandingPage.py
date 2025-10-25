import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit_app.utils.ui_helper import load_css

def show_landing_page(go_to):
    load_css("style.css")

    # Baris atas: SmartBin + tombol Login/Register sejajar
    top_col1, top_col2, top_col3 = st.columns([3, 1, 1])
    with top_col1:
        st.markdown("<h1 class='title'>SmartBin</h1>", unsafe_allow_html=True)
    with top_col2:
        if st.button("Login", key="login_btn"):
            go_to("LoginPage")
    with top_col3:
        if st.button("Register", key="register_btn"):
            go_to("RegisterPage")

    # Welcome Section
    st.markdown("<div class='landing-header'>", unsafe_allow_html=True)
    st.markdown("<h2>Welcome to SmartBin</h2>", unsafe_allow_html=True)
    st.markdown("<h4>Track, Monitor, and Stay Clean...</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Gambar
    img_path = Path(__file__).resolve().parent.parent / "streamlit_app/assets/sampah.png"
    try:
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
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

    # Footer
    st.markdown("""
    <div class='italic'>
    Bersama kita wujudkan kebersihan berkelanjutan  
    Mulai langkah kecil untuk bumi yang lebih hijau
    </div>
    <div class='footer'>
        <b>3 D4 Teknik Komputer A</b><br>
        @SmartBin
    </div>
    """, unsafe_allow_html=True)