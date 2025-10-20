import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt 
import numpy as np
import pymongo
import random

# --- MOCK DATA UNTUK UI ---
class MockSensorsCollection:
    def find(self, query):
        data = []
        start_date = datetime.now() - timedelta(days=7)
        for i in range(100):
            data.append({
                "timestamp": start_date + timedelta(hours=i * 2),
                "kapasitas": np.random.randint(20, 100), 
                "suhu": np.random.uniform(28, 35),
                "kelembapan": np.random.uniform(50, 80),
                "type": "data"
            })
        return data
    def sort(self, key, direction):
        return self.find({})
    def count_documents(self, query):
        return 100

sensors = MockSensorsCollection()

# Fungsi get data (menggunakan mock)
def get_sensor_data(start_date, end_date):
    all_data = sensors.find({})
    data = [d for d in all_data if start_date <= d['timestamp'] <= end_date]
    return data

# Fungsi DONUT CHART generator
def donut_chart_generator(value, title_text, color_range):
    # Pastikan value dalam rentang 0-100
    value = max(0, min(100, value))
    pie_data = pd.DataFrame({'value': [value, 100 - value], 'category': ['Used', 'Empty']})
    
    chart = alt.Chart(pie_data).mark_arc(outerRadius=70, innerRadius=55).encode(
        theta=alt.Theta("value", stack=True),
        color=alt.Color("category", scale=alt.Scale(domain=['Used', 'Empty'], range=color_range), legend=None),
        order=alt.Order("value", sort="descending")
    ).properties(
        title="",
        width=180,
        height=180
    ).configure_view(stroke=None)
    
    st.altair_chart(chart, use_container_width=True)
    st.markdown(f"<p style='text-align: center; margin-top: -10px;'>{title_text}</p>", unsafe_allow_html=True)


def show():
    # Inisialisasi session state
    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = get_sensor_data(datetime.now() - timedelta(days=7), datetime.now())
        
    # --- STYLING CSS GLOBAL ---
    st.markdown(
        """
        <style>
        /* 1. Latar Belakang: Ungu Muda Solid */
        .stApp {
            background-color: #C3B0E1; 
            background: #C3B0E1; 
            color: black;
            font-family: 'Arial', sans-serif;
        }
        
        /* 2. Styling Header (SmartBin Kiri, Home Kanan) */
        .header-text {
            font-weight: bold; 
            font-size: 1.2em;
        }
        .stButton button {
            background-color: black;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
            width: auto;
            white-space: nowrap;
        }
        
        /* 3. Styling Dropdown/Filter Buttons (KOTAK PUTIH MEMBULAT) */
        div[data-testid="stSelectbox"] > div:first-child,
        div[data-testid="stDateInput"] > div:first-child {
            background-color: white !important;
            border-radius: 10px !important;
            border: 1px solid #ccc !important;
            padding: 5px 10px;
            width: 100%;
        }

        /* 4. Kontainer Filter (PENTING: Margin untuk menurunkan konten) */
        .filter-container-wrapper {
             margin-top: 80px; 
        }

        /* 5. Styling Judul Tabel & Log */
        .table-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .log-entry {
            margin-bottom: 5px;
            font-size: 1.0em;
        }
        .footer-text {
            margin-top: 40px;
            font-style: italic;
            color: black;
        }
        
        /* 6. Styling Custom Tabel Header untuk latar belakang putih */
        div[data-testid="stDataFrame"] {
            margin-bottom: 30px;
            border-radius: 10px; /* Sudut membulat untuk dataframe */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- HEADER (SmartBin Kiri, Home Kanan) ---
    header_col1, header_col2 = st.columns([1, 0.15]) 
    
    with header_col1:
        st.markdown('<div class="header-text">SmartBin</div>', unsafe_allow_html=True)
    with header_col2:
        if st.button("Home", key="home_button"): 
            st.session_state.page("Homepage")
            
    # --- WRAPPER UNTUK MENURUNKAN KONTEN FILTER & CHART ---
    st.markdown('<div class="filter-container-wrapper">', unsafe_allow_html=True)

    # --- FILTER WAKTU (3 KOLOM: Rentang, Tanggal, Filter) ---
    col1, col2, col3 = st.columns([1.5, 1.5, 1.5]) 
    
    with col1:
        rentang = st.selectbox("Rentang Waktu", ["7 Hari Terakhir", "30 Hari Terakhir", "Custom"], label_visibility="collapsed", key="rentang_select")
        
    with col2:
        selected_date = st.date_input("Tanggal", datetime.now().date(), label_visibility="collapsed", key="selected_date_input")

    with col3:
        filter_option = st.selectbox(
            "Filter", 
            ["semua", "kapasitas sampah", "suhu dan kelembapan"], 
            label_visibility="collapsed", 
            key="filter_select"
        )
        
    # --- LOGIKA FILTERING & PERHITUNGAN ---
    
    # 1. Tentukan rentang waktu untuk filtering data
    if rentang == "7 Hari Terakhir":
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
    elif rentang == "30 Hari Terakhir":
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
    else: # Custom
        end_date = datetime.combine(selected_date, datetime.max.time())
        start_date = end_date - timedelta(days=7) 
        
    df_raw = pd.DataFrame(get_sensor_data(start_date, end_date))
    df_filtered = df_raw.copy()

    # Hitung Rata-rata Kapasitas dan Suhu/Kelembapan berdasarkan filter
    avg_kapasitas = 0
    avg_suhu_kelembapan = 0

    if not df_filtered.empty:
        if filter_option in ["semua", "kapasitas sampah"]:
            avg_kapasitas = df_filtered['kapasitas'].mean()
        
        if filter_option in ["semua", "suhu dan kelembapan"]:
            avg_suhu = df_filtered['suhu'].mean()
            avg_kelembapan = df_filtered['kelembapan'].mean()
            avg_suhu_kelembapan = (avg_suhu + avg_kelembapan) / 2
        
        if filter_option == "kapasitas sampah" and avg_kapasitas == 0:
             avg_kapasitas = df_raw['kapasitas'].mean()
        if filter_option == "suhu dan kelembapan" and avg_suhu_kelembapan == 0:
             avg_suhu_kelembapan = (df_raw['suhu'].mean() + df_raw['kelembapan'].mean()) / 2
    
    chart1_value = int(avg_kapasitas)
    chart2_value = int(avg_suhu_kelembapan)
    
    # --- VISUALISASI CHART (DINAMIS) ---
    
    col_chart1, col_chart2 = st.columns([1, 1])
    
    # Chart Kapasitas
    with col_chart1:
        if filter_option != "suhu dan kelembapan":
            donut_chart_generator(
                value=chart1_value,
                title_text="Rata-rata kapasitas sampah per hari selama 7 hari terakhir",
                color_range=['#6B48FF', '#E0E0E0']
            )
        else:
             st.markdown("<p style='text-align: center; height: 180px;'></p>", unsafe_allow_html=True) # Spacer
    
    # Chart Suhu & Kelembapan
    with col_chart2:
        if filter_option != "kapasitas sampah":
            donut_chart_generator(
                value=chart2_value,
                title_text="Rata-rata suhu & kelembapan selama 7 hari terakhir",
                color_range=['#FF8C00', '#E0E0E0']
            )
        else:
             st.markdown("<p style='text-align: center; height: 180px;'></p>", unsafe_allow_html=True) # Spacer

    st.markdown('</div>', unsafe_allow_html=True) # Penutup filter-container-wrapper

    # --- TABEL RIWAYAT ---
    st.markdown("<div class='table-title'>Tabel Riwayat</div>", unsafe_allow_html=True)
    
    df_table = df_raw.copy()
    columns_to_show = ['timestamp', 'kapasitas', 'suhu', 'kelembapan']
    
    if filter_option == "kapasitas sampah":
        columns_to_show = ['timestamp', 'kapasitas']
    elif filter_option == "suhu dan kelembapan":
        columns_to_show = ['timestamp', 'suhu', 'kelembapan']
    
    df_display = df_table.rename(columns={'timestamp': '⏰ Waktu', 'kapasitas': '🗑️ Kapasitas (%)', 'suhu': '🌡️ Suhu (°C)', 'kelembapan': '💧 Kelembapan (%)'})

    # 1. Tabel Waktu & Kapasitas
    if 'kapasitas' in columns_to_show or filter_option == "semua":
        st.markdown("""
            <div class="custom-table-header">
                <span style="width: 50%;">⏰ Waktu</span>
                <span style="width: 50%; text-align: right;">🗑️ Kapasitas (%)</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.dataframe(df_display[['⏰ Waktu', '🗑️ Kapasitas (%)']], 
                     hide_index=True, 
                     column_config={
                         '⏰ Waktu': st.column_config.DatetimeColumn('⏰ Waktu', format="HH:mm:ss"),
                         '🗑️ Kapasitas (%)': st.column_config.NumberColumn('🗑️ Kapasitas (%)', format="%d%%")
                     },
                     use_container_width=True,
                     height=300) # PERBAIKAN: Tinggi diubah menjadi 300px

    # 2. Tabel Suhu & Kelembapan
    if 'suhu' in columns_to_show or filter_option == "semua":
        st.markdown("""
            <div class="custom-table-header" style="margin-top: 20px;">
                <span style="width: 50%;">🌡️ Suhu (°C)</span>
                <span style="width: 50%; text-align: right;">💧 Kelembapan (%)</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.dataframe(df_display[['🌡️ Suhu (°C)', '💧 Kelembapan (%)']], 
                     hide_index=True, 
                     column_config={
                         '🌡️ Suhu (°C)': st.column_config.NumberColumn('🌡️ Suhu (°C)', format="%.1f°C"),
                         '💧 Kelembapan (%)': st.column_config.NumberColumn('💧 Kelembapan (%)', format="%d%%")
                     },
                     use_container_width=True,
                     height=300) # PERBAIKAN: Tinggi diubah menjadi 300px
    
    # --- LOG ---
    st.markdown("<div class='table-title'>Log</div>", unsafe_allow_html=True)
    
    log_entries = [
        f"📅 {datetime.now().strftime('%d/%m/%Y')}",
        "[10:20] Tempat sampah penuh",
        "[08:45] Kantong diganti",
        "[Kemarin] Suhu di atas batas normal"
    ]
    
    for i, entry in enumerate(log_entries):
        if i == 0:
            st.markdown(f"<h3>{entry}</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='log-entry'>{entry}</p>", unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown(
        """
        <div class="footer-text">
        3 D4 Teknik Komputer A
        <br>
        @SmartBin
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show()