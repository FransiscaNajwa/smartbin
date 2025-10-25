import streamlit as st
from streamlit_app.utils.ui_helper import load_css

def show_notifikasi_page(go_to=None):
    load_css("style.css")

    # Header teks
    st.markdown("""
    <div class="centered-text" style="margin-top:10px;">
        <h1>Welcome to Notifikasi Page</h1>
    </div>
""", unsafe_allow_html=True)
    
    # Kategori: Kapasitas Sampah
    st.subheader("📦 Kategori: Kapasitas Sampah")

    st.markdown("**1. Tempat sampah hampir penuh (80%)**")
    st.markdown("- Waktu: 05 Okt 2025, 10:45 WIB")
    st.markdown("- Pesan: Tempat sampah di dalam gedung hampir penuh. Segera lakukan pengosongan sebelum meluap.")

    st.markdown("**2. Tempat sampah penuh (100%)**")
    st.markdown("- Waktu: 05 Okt 2025, 18:22 WIB")
    st.markdown("- Pesan: Tempat sampah di luar gedung penuh. Mohon kosongkan secepatnya.")

    st.markdown("---")

    # Kategori: Suhu & Kelembapan
    st.subheader("🌡️ Kategori: Suhu & Kelembapan")

    st.markdown("**1. Suhu meningkat di atas ambang batas (35°C)**")
    st.markdown("- Waktu: 04 Okt 2025, 13:15 WIB")
    st.markdown("- Pesan: Suhu meningkat di dalam tempat sampah melebihi ambang batas. Periksa kemungkinan adanya proses kimia.")

    st.markdown("**2. Kelembapan terlalu tinggi (85%)**")
    st.markdown("- Waktu: 03 Okt 2025, 09:00 WIB")
    st.markdown("- Pesan: Kelembapan di dalam tempat sampah meningkat. Periksa kondisi sisa makanan atau kantong sampah.")

    st.markdown("---")

    # Tombol navigasi kembali
    if st.button("⬅️ Back"):
        if go_to:
            go_to("HomePage")
# Footer
    st.markdown("""
    <div class='footer'>
        <b>3 D4 Teknik Komputer A</b><br>
        <b>@SmartBin</b>
    </div>
    """, unsafe_allow_html=True)