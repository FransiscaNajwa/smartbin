import streamlit as st
from app.utils.ui_helper import load_css
from PIL import Image
from pathlib import Path
from io import BytesIO
import base64
from datetime import datetime
from app.database.sensor_crud import get_latest_data
from app.database.notification_helper import generate_notifications_from_data

# === Halaman Utama ===
def show_home_page(go_to):
    load_css("style.css")

    # 🧭 Navigasi Atas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("👤 Profil", use_container_width=True):
            go_to("ProfilePage")
    with col2:
        if st.button("📜 Riwayat", use_container_width=True):
            go_to("RiwayatPage")
    with col3:
        if st.button("🔔 Notifikasi", use_container_width=True):
            go_to("NotifikasiPage")
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            go_to("LoginPage")

    # 🖼️ Header & Gambar
    st.markdown("<h1 class='page-title'>Selamat Datang di SmartBin</h1>", unsafe_allow_html=True)

    img_path = Path(__file__).resolve().parent.parent / "app/assets/sampah.png"
    try:
        image = Image.open(img_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        st.markdown(f"""
            <div style='text-align:center;'>
                <img src="data:image/png;base64,{img_base64}" 
                     style="width:700px; border-radius:20px; margin-top:10px;">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Gambar 'sampah.png' tidak ditemukan di folder assets.")

    # 📊 Ambil Data Sensor Terbaru
    device_id = "bin001"
    latest = get_latest_data(limit=10, device_id=device_id) or []

    kapasitas = suhu = kelembapan = status = "-"
    timestamp = "-"

    for sensor in ["capacity", "temperature", "humidity"]:
        data = next((d for d in latest if d["sensor_type"] == sensor), None)
        if data:
            val = data["value"]
            if sensor == "capacity":
                kapasitas = f"{val}%"
                timestamp = data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                status = (
                    "Penuh" if val >= 100
                    else "Hampir Penuh" if val >= 80
                    else "Cukup" if val >= 50
                    else "Rendah"
                )
            elif sensor == "temperature":
                suhu = f"{val}°C"
            elif sensor == "humidity":
                kelembapan = f"{val}%"

    # 🌡️ Monitoring Section
    st.markdown("<h3 class='section-title' style='margin-top:60px;'>📊 Monitoring Data</h3>", unsafe_allow_html=True)

    # Tampilkan data
    st.markdown("<div class='info-label'>🗑️ Kapasitas Tempat Sampah (%)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-card'>{kapasitas}</div>", unsafe_allow_html=True)

    st.markdown("<div class='info-label'>🌡️ Suhu (°C)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-card'>{suhu}</div>", unsafe_allow_html=True)

    st.markdown("<div class='info-label'>💧 Kelembapan (%)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-card'>{kelembapan}</div>", unsafe_allow_html=True)

    st.markdown("<div class='info-label'>⚙️ Status</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-card'>{status}</div>", unsafe_allow_html=True)

    st.caption(f"📅 Data terakhir: {timestamp}")

    # 🔔 Notifikasi
    st.markdown("<h3 class='section-title'>🔔 Notifikasi</h3>", unsafe_allow_html=True)
    notifications = generate_notifications_from_data(latest)

    if notifications:
        for n in notifications:
            waktu = n.get("timestamp")
            if isinstance(waktu, datetime):
                waktu = waktu.strftime("%d %b %Y, %H:%M WIB")
            else:
                waktu = "-"

            msg = (
                f"🔔 <b>{n['category'].capitalize()}</b> — {n['message']}<br>"
                f"📅 {waktu} | 📈 {n['value']}{n['unit']}"
            )
            st.markdown(f"<div class='notif-box'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.success("✅ Tidak ada notifikasi. Semua kondisi normal.")

    # 🦶 Footer
    st.markdown("""
        <div class='footer' style='text-align:center; margin-top:200px;'>
            <p><b>3 D4 Teknik Komputer A</b><br>@SmartBin</p>
        </div>
    """, unsafe_allow_html=True)
