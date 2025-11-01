import streamlit as st
import pandas as pd
import altair as alt
from app.utils.ui_helper import load_css
from app.database.sensor_crud import get_latest_data


def show_riwayat_page(go_to):
    # Muat CSS
    load_css("style.css")

    # Judul halaman
    st.markdown("<h1 class='section-title'>Halaman Riwayat</h1>", unsafe_allow_html=True)

    # Ambil data sensor dari MongoDB
    sensor_data = get_latest_data(limit=50)

    # Siapkan DataFrame kosong untuk tampilan awal
    df_all = pd.DataFrame(columns=["Waktu", "Kapasitas", "Suhu", "Kelembapan", "Status"])

    if not sensor_data:
        st.warning("⚠️ Tidak ada data sensor ditemukan.")
    else:
        # Ubah data ke DataFrame
        df = pd.DataFrame(sensor_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Pivot data agar setiap waktu jadi satu baris
        df_pivot = df.pivot_table(
            index="timestamp",
            columns="sensor_type",
            values="value",
            aggfunc="first"
        ).reset_index()

        # Ubah nama kolom agar rapi
        df_pivot.rename(columns={
            "timestamp": "Waktu",
            "capacity": "Kapasitas",
            "temperature": "Suhu",
            "humidity": "Kelembapan"
        }, inplace=True)

        # Tentukan status berdasarkan kapasitas
        def get_status(cap):
            if pd.isna(cap):
                return "-"
            if cap >= 100:
                return "Penuh"
            elif cap >= 80:
                return "Hampir Penuh"
            elif cap >= 50:
                return "Cukup"
            else:
                return "Rendah"

        df_pivot["Status"] = df_pivot["Kapasitas"].apply(get_status)

        # Urutkan berdasarkan waktu
        df_all = df_pivot.sort_values("Waktu", ascending=True)

    # === BAGIAN TABEL ===
    st.markdown("### 📋 Tabel Riwayat")
    st.dataframe(df_all, use_container_width=True)

    # === BAGIAN GRAFIK ===
    st.markdown("<hr><br>", unsafe_allow_html=True)
    st.markdown("### 📊 Grafik")

    if df_all.empty:
        st.info("📉 Belum ada data untuk ditampilkan dalam grafik.")
    else:
        # Ubah data ke format long agar bisa multi-line chart
        df_melt = df_all.melt(
            id_vars=["Waktu"],
            value_vars=["Kapasitas", "Suhu", "Kelembapan"],
            var_name="Sensor",
            value_name="Nilai"
        )

        # Buat chart dengan Altair
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Waktu:T", title="Waktu"),
            y=alt.Y("Nilai:Q", title="Nilai Sensor"),
            color=alt.Color("Sensor:N", title="Jenis Sensor"),
            tooltip=["Waktu", "Sensor", "Nilai"]
        ).properties(
            width="container",
            height=350,
            title="Grafik Kapasitas, Suhu, dan Kelembapan"
        )

        st.altair_chart(chart, use_container_width=True)

    # === SPASI & TOMBOL NAVIGASI ===
    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("Kembali"):
        go_to("HomePage")

    # === FOOTER (SELALU TAMPIL) ===
    st.markdown(
        """
        <div class='footer' style='text-align:center; margin-top:200px; color:black;'>
            <p><b>3 D4 Teknik Komputer A</b><br>@SmartBin</p>
        </div>
        """,
        unsafe_allow_html=True
    )
