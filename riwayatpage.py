import streamlit as st
import pymongo
import pandas as pd
from datetime import datetime, timedelta

# Koneksi MongoDB (ganti dengan connection string Anda)
client = pymongo.MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/smartbin_db")
db = client.smartbin_db
sensors = db.sensors

def show():
    # Judul dan navigasi
    st.title("Riwayat Page")
    st.button("Home", on_click=lambda: st.session_state.page("Homepage"))

    # Warna latar belakang dan styling button
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to right, #C3B1E1, #B0C4DE);
        }
        .stButton {
            background-color: #ffe6e6;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Filter waktu
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        rentang = st.selectbox("Rentang Waktu", ["7 Hari Terakhir", "Custom"])
    with col2:
        start_date = st.date_input("Tanggal Mulai", datetime.now() - timedelta(days=7))
    with col3:
        end_date = st.date_input("Tanggal Akhir", datetime.now())

    if st.button("Filter"):
        query = {"timestamp": {"$gte": start_date, "$lte": end_date}}
        data = list(sensors.find(query).sort("timestamp", -1))

        if data:
            df = pd.DataFrame(data)

            # Rata-rata Kapasitas 7 Hari
            st.markdown("<h3 style='text-align: center;'>Rata-rata Kapasitas Sampah per Hari</h3>", unsafe_allow_html=True)
            kapasitas_avg = df.groupby(df['timestamp'].dt.date)['kapasitas'].mean()
            st.bar_chart(kapasitas_avg)

            # Rata-rata Suhu & Kelembapan
            st.markdown("<h3 style='text-align: center;'>Rata-rata Suhu & Kelembapan</h3>", unsafe_allow_html=True)
            suhu_avg = df['suhu'].mean()
            kelembapan_avg = df['kelembapan'].mean()
            col1, col2 = st.columns(2)
            col1.metric("Suhu Rata-rata", f"{suhu_avg:.1f}°C")
            col2.metric("Kelembapan Rata-rata", f"{kelembapan_avg:.1f}%")

            # Tabel Riwayat
            st.markdown("<h3 style='text-align: center;'>Tabel Riwayat</h3>", unsafe_allow_html=True)
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write("⏰ Waktu")
                with col2:
                    st.write("🗑️ Kapasitas (%)")
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write("🌡️ Suhu (°C)")
                with col2:
                    st.write("💧 Kelembapan (%)")
            st.dataframe(df[['timestamp', 'kapasitas', 'suhu', 'kelembapan']])

            # Log
            st.markdown("<h3 style='text-align: center;'>Log</h3>", unsafe_allow_html=True)
            for entry in data:
                st.write(f"[{entry['timestamp'].strftime('%H:%M')}] {entry['type']}: {entry['value']}")
        else:
            st.info("Tidak ada data untuk rentang waktu ini.")

    # Footer
    st.markdown(
        """
        <div style='text-align: center; margin-top: 60px; font-style: italic; color: black;'>
        D4 Teknik Komputer A @SmartBin
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()