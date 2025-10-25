import streamlit as st
from streamlit_app.utils.ui_helper import load_css
from PIL import Image
from pathlib import Path
from io import BytesIO
import base64
from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta
from app.database.crud_operations import get_latest_data, get_sensor_data_by_date

def show_home_page(go_to):
    load_css("style.css")

    # Header
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to SmartBin</h1>
            <h3>Track, Monitor, Stay Clean</h3>
        </div>
    """, unsafe_allow_html=True)

    # Gambar SmartBin
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

    # Monitoring Section
    st.markdown("<div class='section-title'>Monitoring</div>", unsafe_allow_html=True)
    device_id = "bin001"

    latest = get_latest_data(limit=10, device_id=device_id)
    kapasitas = suhu = kelembapan = "-"
    timestamp = "-"

    for sensor in ["capacity", "temperature", "humidity"]:
        data = next((d for d in latest if d["sensor_type"] == sensor), None)
        if data:
            if sensor == "capacity":
                kapasitas = f"{data['value']}%"
                timestamp = data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            elif sensor == "temperature":
                suhu = f"{data['value']}°C"
            elif sensor == "humidity":
                kelembapan = f"{data['value']}%"

    st.markdown("🗑️ **Kapasitas Tempat Sampah (%)**")
    st.markdown(f"<div class='info-card'>{kapasitas}</div>", unsafe_allow_html=True)
    st.markdown("🌡️ **Suhu (°C)**")
    st.markdown(f"<div class='info-card'>{suhu}</div>", unsafe_allow_html=True)
    st.markdown("💧 **Kelembapan (%)**")
    st.markdown(f"<div class='info-card'>{kelembapan}</div>", unsafe_allow_html=True)
    st.caption(f"📅 Data terakhir: {timestamp}")

    # Riwayat Section
    st.markdown("<div class='section-title'>Riwayat</div>", unsafe_allow_html=True)
    filter_option = st.radio("Filter berdasarkan:", ["Hari", "Minggu", "Bulan"], horizontal=True)

    def render_table(raw):
        grouped = defaultdict(dict)
        for d in raw:
            waktu = d["timestamp"].strftime("%d/%m %H:%M")
            grouped[waktu][d["sensor_type"]] = d["value"]

        df = pd.DataFrame([
            {
                "🕓 Waktu": waktu,
                "🗑️ Kapasitas (%)": group.get("capacity", "-"),
                "🌡️ Suhu (°C)": group.get("temperature", "-"),
                "💧 Kelembapan (%)": group.get("humidity", "-")
            }
            for waktu, group in grouped.items()
        ])
        if df.empty:
            st.warning("⚠️ Tidak ada data sensor untuk rentang tersebut.")
        else:
            df = df.sort_values("🕓 Waktu", ascending=False)
            st.table(df)

    if filter_option == "Hari":
        selected_date = st.date_input("Pilih tanggal")
        st.markdown(f"#### Riwayat untuk tanggal: {selected_date.strftime('%d/%m/%Y')}")
        raw = get_sensor_data_by_date(selected_date.strftime("%Y-%m-%d"), device_id=device_id)
        render_table(raw)

    elif filter_option == "Minggu":
        reference_date = st.date_input("Pilih tanggal referensi minggu")
        selected_week = st.number_input("Minggu ke berapa dari tanggal itu?", min_value=1, max_value=52, step=1)
        start_date = reference_date + timedelta(weeks=selected_week - 1)
        start_date -= timedelta(days=start_date.weekday())  # Mulai dari Senin
        end_date = start_date + timedelta(days=6)

        st.markdown(f"#### Riwayat untuk minggu ke-{selected_week} ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')})")

        all_data = []
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            all_data.extend(get_sensor_data_by_date(date, device_id=device_id))
        render_table(all_data)

    elif filter_option == "Bulan":
        bulan_dict = {
            "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
            "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
            "September": 9, "Oktober": 10, "November": 11, "Desember": 12
        }
        selected_month = st.selectbox("Pilih bulan", list(bulan_dict.keys()))
        current_year = datetime.now().year
        month_num = bulan_dict[selected_month]
        start_date = datetime(current_year, month_num, 1)
        if month_num == 12:
            end_date = datetime(current_year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(current_year, month_num + 1, 1) - timedelta(days=1)

        st.markdown(f"#### Riwayat untuk bulan: {selected_month} ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')})")

        all_data = []
        for i in range((end_date - start_date).days + 1):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            all_data.extend(get_sensor_data_by_date(date, device_id=device_id))
        render_table(all_data)

    # Navigasi
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