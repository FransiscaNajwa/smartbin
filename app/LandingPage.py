# import streamlit as st
# from PIL import Image
# from pathlib import Path
# from streamlit_app.utils.ui_helper import load_css
# from app.database.crud_operations import get_latest_data
# import base64
# from io import BytesIO
# import pandas as pd
# from collections import defaultdict
# from streamlit_autorefresh import st_autorefresh

# # Refresh otomatis setiap 10 detik
# st_autorefresh(interval=10 * 1000, key="landing_refresh")

# def show_landing_page(go_to):
#     load_css("style.css")

#     # Header
#     st.markdown("""
#         <div class='landing-header'>
#             <h2>Welcome to SmartBin</h2>
#             <h4>Track, Monitor, and Stay Clean</h4>
#         </div>
#     """, unsafe_allow_html=True)

#     # Gambar
#     img_path = Path(__file__).resolve().parent.parent / "streamlit_app/assets/sampah.png"
#     try:
#         image = Image.open(img_path)
#         buffered = BytesIO()
#         image.save(buffered, format="PNG")
#         img_base64 = base64.b64encode(buffered.getvalue()).decode()

#         st.markdown(f"""
#             <div class='welcome-section'>
#                 <img src="data:image/png;base64,{img_base64}" class="responsive-img">
#             </div>
#         """, unsafe_allow_html=True)
#     except Exception as e:
#         st.warning(f"⚠️ Gagal memuat gambar: {e}")

#     # Ambil data sensor terbaru untuk 1 device
#     device_id = "bin001"
#     latest = get_latest_data(10, device_id=device_id)

#     # Inisialisasi
#     kapasitas = suhu = kelembapan = "-"
#     timestamp = "-"

#     # Ambil data terbaru per sensor
#     for sensor in ["capacity", "temperature", "humidity"]:
#         data = next((d for d in latest if d["sensor_type"] == sensor), None)
#         if data:
#             if sensor == "capacity":
#                 kapasitas = f"{data['value']}%"
#                 timestamp = data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
#             elif sensor == "temperature":
#                 suhu = f"{data['value']}°C"
#             elif sensor == "humidity":
#                 kelembapan = f"{data['value']}%"

#     # Monitoring Preview
#     st.markdown("<div class='section-title'>Monitoring Page</div>", unsafe_allow_html=True)
#     st.markdown("🗑️ **Kapasitas Tempat Sampah (%)**")
#     st.markdown(f"<div class='info-card'>{kapasitas}</div>", unsafe_allow_html=True)
#     st.markdown("🌡️ **Suhu (°C)**")
#     st.markdown(f"<div class='info-card'>{suhu}</div>", unsafe_allow_html=True)
#     st.markdown("💧 **Kelembapan (%)**")
#     st.markdown(f"<div class='info-card'>{kelembapan}</div>", unsafe_allow_html=True)
#     st.caption(f"📅 Data terakhir: {timestamp}")

#     # Riwayat Preview
#     st.markdown("<div class='section-title'>Riwayat Page</div>", unsafe_allow_html=True)
#     if latest:
#         grouped = defaultdict(dict)
#         for d in latest:
#             waktu = d["timestamp"].strftime("%H:%M")
#             grouped[waktu][d["sensor_type"]] = d["value"]

#         df = pd.DataFrame([
#             {
#                 "🕓 Waktu": waktu,
#                 "🗑️ Kapasitas (%)": group.get("capacity"),
#                 "🌡️ Suhu (°C)": group.get("temperature"),
#                 "💧 Kelembapan (%)": group.get("humidity")
#             }
#             for waktu, group in grouped.items()
#         ])
#         df = df.sort_values("🕓 Waktu", ascending=False)
#         st.table(df)
#     else:
#         st.warning("⚠️ Belum ada data sensor untuk device ini.")

#     # How it works
#     st.markdown("<div class='section-title'>How it works?</div>", unsafe_allow_html=True)
#     st.markdown("""
#     **1. Hubungkan Perangkat IoT**  
#     Sambungkan sensor dengan WiFi dan sistem SmartBin  

#     **2. Pantau dari Website**  
#     Login dan lihat status tempat sampah secara real-time  

#     **3. Dapatkan Notifikasi**  
#     Terima peringatan ketika tempat sampah penuh dan suhu dalam tempat sampah meningkat
#     """)

#     # Tombol Login dan Register
#     st.markdown("---")
#     if st.button("Login"):
#         go_to("LoginPage")
#     if st.button("Register"):
#         go_to("RegisterPage")

#     # Footer
#     st.markdown("""
#     <div class='italic'>
#         <b>Bersama kita wujudkan kebersihan berkelanjutan</b><br>
#         <b>Mulai langkah kecil untuk bumi yang lebih hijau</b>
#     </div>
#     <div class='footer'>
#         <b>3 D4 Teknik Komputer A</b><br>
#         <b>@SmartBin</b>
#     </div>
#     """, unsafe_allow_html=True)