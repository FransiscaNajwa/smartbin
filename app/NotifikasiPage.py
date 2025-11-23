import streamlit as st
from datetime import datetime
from app.utils.ui_helper import load_css
from app.database.sensor_crud import get_latest_data
from app.database.notification_helper import detect_notification

def show_notifikasi_page(go_to=None):
    load_css("style.css")

    st.markdown("""
        <div class="centered-text" style="margin-top:10px;">
            <h1>Halaman Notifikasi</h1>
        </div>
    """, unsafe_allow_html=True)

    # 📊 Ambil data sensor terbaru
    data = get_latest_data(limit=200)

    # 🔍 Gunakan helper detect_notification agar konsisten dengan Telegram
    notif_list = []
    for d in data:
        detected = detect_notification(d)
        if detected:
            notif_list.extend(detected)

    # Urutkan notifikasi dari terbaru ke terlama
    notif_list.sort(key=lambda x: x.get("timestamp", datetime.min), reverse=True)

    # ==========================================
    # 🗑️ NOTIFIKASI KAPASITAS TEMPAT SAMPAH
    # ==========================================
    st.subheader("📦 Kapasitas Tempat Sampah")

    kapasitas_notif = [n for n in notif_list if n["category"] == "kapasitas"]
    if kapasitas_notif:
        for i, n in enumerate(kapasitas_notif, 1):
            waktu = n.get("timestamp")
            waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if isinstance(waktu, datetime) else "-"
            st.markdown(f"**{i}. Tempat sampah {n['level']} ({n['value']}{n['unit']})**")
            st.markdown(f"- Waktu: {waktu_str}")
            st.markdown(f"- Pesan: {n['message']}")
    else:
        st.info("ℹ️ Belum ada notifikasi kapasitas.")

    st.markdown("---")

    # ==========================================
    # 🌡️ NOTIFIKASI SUHU & KELEMBAPAN
    # ==========================================
    st.subheader("🌡️ Suhu & Kelembapan")

    suhu_notif = [n for n in notif_list if n["category"] == "suhu"]
    kelembapan_notif = [n for n in notif_list if n["category"] == "kelembapan"]

    # ====== NOTIFIKASI SUHU ======
    if suhu_notif:
        for i, n in enumerate(suhu_notif, 1):
            waktu = n.get("timestamp")
            waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if isinstance(waktu, datetime) else "-"
            st.markdown(f"**{i}. Suhu meningkat ({n['value']}{n['unit']})**")
            st.markdown(f"- Waktu: {waktu_str}")
            st.markdown(f"- Pesan: {n['message']}")
    else:
        st.info("ℹ️ Belum ada notifikasi suhu.")

    # ====== NOTIFIKASI KELEMBAPAN ======
    if kelembapan_notif:
        for i, n in enumerate(kelembapan_notif, 1):
            waktu = n.get("timestamp")
            waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if isinstance(waktu, datetime) else "-"
            st.markdown(f"**{i}. Kelembapan tinggi ({n['value']}{n['unit']})**")
            st.markdown(f"- Waktu: {waktu_str}")
            st.markdown(f"- Pesan: {n['message']}")
    else:
        st.info("ℹ️ Belum ada notifikasi kelembapan.")

    st.markdown("---")

    # Tombol navigasi kembali
    if st.button("Kembali"):
        if go_to:
            go_to("HomePage")

    # Footer
    st.markdown("""
        <div class='footer' style='text-align:center; margin-top:200px;'>
            <p><b>3 D4 Teknik Komputer A</b><br>@SmartBin</p>
        </div>
    """, unsafe_allow_html=True)