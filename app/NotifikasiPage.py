import streamlit as st
from app.utils.ui_helper import load_css
from app.database.sensor_crud import get_latest_data

def show_notifikasi_page(go_to=None):
    load_css("style.css")

    st.markdown("""
        <div class="centered-text" style="margin-top:10px;">
            <h1>Halaman Notifikasi</h1>
        </div>
    """, unsafe_allow_html=True)

    # 📊 Ambil data sensor terbaru
    data = get_latest_data(limit=200)

    # ==========================================
    # 🗑️ NOTIFIKASI KAPASITAS TEMPAT SAMPAH
    # ==========================================
    st.subheader("📦 Kapasitas Tempat Sampah")

    kapasitas_notif = [
        d for d in data
        if d.get("value") is not None and d["value"] >= 80
    ]

    if kapasitas_notif:
        for i, d in enumerate(kapasitas_notif, 1):
            val = d["value"]
            level = "penuh" if val >= 90 else "hampir penuh"
            waktu = d.get("timestamp")
            waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if waktu else "-"

            pesan = (
                "Tempat sampah penuh. Mohon kosongkan secepatnya."
                if level == "penuh"
                else "Tempat sampah hampir penuh. Segera lakukan pengosongan."
            )

            st.markdown(f"**{i}. Tempat sampah {level} ({val}%)**")
            st.markdown(f"- Waktu: {waktu_str}")
            st.markdown(f"- Pesan: {pesan}")
    else:
        st.info("ℹ️ Belum ada notifikasi kapasitas.")

    st.markdown("---")

    # ==========================================
    # 🌡️ NOTIFIKASI SUHU & KELEMBAPAN
    # ==========================================
    st.subheader("🌡️ Suhu & Kelembapan")

    # suhu > 35
    suhu_notif = [
        d for d in data
        if d.get("temperature") is not None and d["temperature"] > 35
    ]

    # kelembapan > 85
    kelembapan_notif = [
        d for d in data
        if d.get("humidity") is not None and d["humidity"] > 85
    ]

    # ====== NOTIFIKASI SUHU ======
    if suhu_notif:
        for i, d in enumerate(suhu_notif, 1):
            waktu = d.get("timestamp")
            waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if waktu else "-"

            st.markdown(f"**{i}. Suhu meningkat ({d['temperature']}°C)**")
            st.markdown(f"- Waktu: {waktu_str}")
            st.markdown("- Pesan: Suhu melebihi ambang batas. Periksa kemungkinan reaksi kimia.")
    else:
        st.info("ℹ️ Belum ada notifikasi suhu.")

    # ====== NOTIFIKASI KELEMBAPAN ======
    if kelembapan_notif:
        for i, d in enumerate(kelembapan_notif, 1):
            waktu = d.get("timestamp")
            waktu_str = waktu.strftime("%d %b %Y, %H:%M WIB") if waktu else "-"

            st.markdown(f"**{i}. Kelembapan tinggi ({d['humidity']}%)**")
            st.markdown(f"- Waktu: {waktu_str}")
            st.markdown("- Pesan: Kelembapan terlalu tinggi. Periksa kondisi sisa makanan.")
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
