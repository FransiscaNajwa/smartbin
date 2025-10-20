import streamlit as st
import pymongo
# import paho.mqtt.client as mqtt
import json
# import threading
import bcrypt
from datetime import datetime

# Koneksi MongoDB (DINONAKTIFKAN)
# client = pymongo.MongoClient("mongodb+srv://smartbinuser:<SmartBin123>@cluster0.inq2nbd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client.smartbin_db
# users = db.users
# sensors = db.sensors

# State untuk data (Mock Data)
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {"kapasitas": 68, "suhu": 32, "kelembapan": 32}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "LandingPage"

# Fungsi navigasi (mengganti page state)
def navigate_to(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

# Fungsi get color berdasarkan status (digunakan di mockup)
def get_status_color(status):
    if status == "Aman":
        return "#FF8C00" 
    return "#FF8C00"

# --- CONFIG & STYLING SESUAI DESAIN ---
st.set_page_config(page_title="SmartBin", page_icon="🗑️", layout="wide")

st.markdown("""
    <style>
    /* 1. Latar Belakang: Ungu Muda Solid */
    .stApp {
        background-color: #C3B0E1; 
        background: #C3B0E1; 
        color: black;
        font-family: 'Arial', sans-serif;
    }
    
    /* 2. Styling Tombol Header (Login/Register) */
    .stButton button {
        background-color: black;
        color: white;
        border-radius: 5px;
        padding: 8px 15px;
        width: auto;
        white-space: nowrap;
        font-weight: bold;
        margin-left: 10px;
    }
    .header-text {
        font-weight: bold; 
        font-size: 1.2em;
    }

    /* 3. Hero Section Text */
    .welcome-title {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0;
    }
    .slogan-text {
        font-size: 1.2em;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    /* 4. Monitoring Mockup Styles */
    .mockup-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 10px;
        text-align: left;
    }
    .value-box-mock {
        display: inline-block;
        border-radius: 10px;
        padding: 8px 12px;
        font-size: 2.0em; 
        font-weight: bold;
        text-align: center;
        color: black; 
        margin-right: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .icon-title-mock {
        font-size: 1em;
        font-weight: bold;
        display: block;
        align-items: center;
        margin-bottom: 5px;
        margin-top: 15px;
        min-height: 40px;
    }

    /* 5. Riwayat Mockup Table Style (DIPERBAIKI UNTUK TEXT-ALIGN: CENTER) */
    .mock-table-container {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 10px;
        margin-bottom: 20px;
        overflow: hidden; 
    }
    
    .table-data-wrapper { max-height: 250px; overflow-y: scroll; }
    .table-row { display: flex; width: 100%; }

    /* Styling Header Kolom */
    .table-header-cell {
        background-color: #f0f0f0; 
        font-weight: bold;
        padding: 10px;
        border-right: 1px solid #ccc;
        width: 50%;
        text-align: center; /* Header dibuat rata tengah */
    }
    
    /* Styling Data Kolom */
    .table-data-cell {
        padding: 8px 10px;
        border-bottom: 1px solid #eee;
        border-right: 1px solid #eee;
        width: 50%;
        text-align: center; /* Data dibuat RATA TENGAH */
    }
    .table-data-cell:last-child {
        border-right: none;
    }
    .table-header-cell:last-child {
        border-right: none;
    }
    .table-title-header {
         font-size: 1.2em;
         font-weight: bold;
         margin-bottom: 5px;
         margin-top: 15px;
         display: flex;
         align-items: center;
    }
    .table-icon {
        margin-right: 5px;
        vertical-align: middle;
    }

    /* 6. Footer Styling */
    .how-it-works-list { list-style-type: none; padding-left: 0; font-style: italic; font-size: 1.1em; }
    .how-it-works-list li { margin-bottom: 10px; }
    .how-it-works-list b { font-size: 1.1em; font-weight: bold; }
    .footer-text { margin-top: 50px; font-style: italic; color: black; }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk render tabel dengan pemusatan
def render_centered_table(title_markdown, data_rows, header_cells):
    # Menggunakan rasio kolom [1, 4, 1] untuk pemusatan
    col_left, col_center, col_right = st.columns([1, 4, 1])

    with col_center:
        st.markdown(title_markdown, unsafe_allow_html=True)
        st.markdown('<div class="mock-table-container">', unsafe_allow_html=True)
        
        # Header Row
        st.markdown(f'<div class="table-row table-header-row">{header_cells}</div>', unsafe_allow_html=True)
        
        # Data Wrapper (SCROLLABLE AREA)
        st.markdown('<div class="table-data-wrapper">', unsafe_allow_html=True)
        for time_val, val2 in data_rows:
            # Karena CSS sekarang mengatur semua data ke tengah, kita hanya perlu mencetak valuenya
            st.markdown(f'<div class="table-row">'
                        f'<div class="table-data-cell">{time_val}</div>'
                        f'<div class="table-data-cell">{val2}</div>'
                        f'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Penutup table-data-wrapper
        
        st.markdown('</div>', unsafe_allow_html=True) # Penutup mock-table-container


def show_landing_page(): 
    
    # Data Dummy
    mock_data_kapasitas = [
        ("11:08:11", "54%"), ("13:08:11", "69%"), ("15:08:11", "45%"), 
        ("17:08:11", "23%"), ("19:08:11", "96%"), ("21:08:11", "78%"), 
        ("23:08:11", "44%"), ("01:08:11", "23%"), ("03:08:11", "88%"), 
        ("05:08:11", "12%"), ("07:08:11", "65%") 
    ]
    mock_data_suhu = [
        ("34.3°C", "52%"), ("34.8°C", "67%"), ("31.4°C", "57%"), 
        ("32.0°C", "60%"), ("33.5°C", "70%")
    ]
    
    # --- 1. HEADER (SmartBin Kiri, Login/Register Kanan) ---
    header_col1, header_col2 = st.columns([1, 0.25]) 
    
    with header_col1:
        st.markdown('<div class="header-text">SmartBin</div>', unsafe_allow_html=True)

    with header_col2:
        nav_col1, nav_col2 = st.columns([1, 1])
        
        with nav_col1:
            if st.button("Register", key="nav_register"): navigate_to("Register")
        with nav_col2:
            if st.button("Login", key="nav_login"): navigate_to("Login")

    # --- HERO SECTION (Judul dan Slogan) ---
    st.markdown('<h1 class="welcome-title">Welcome to SmartBin</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan-text">Track, Monitor, and Stay Clean......</p>', unsafe_allow_html=True)

    # --- GAMBAR UTAMA (Ukuran DIPERBESAR dan Terpusat) ---
    col_img_left, col_img_center, col_img_right = st.columns([0.5, 5, 0.5])
    with col_img_center:
        st.image(
            "sampah.png", 
            use_container_width=True,
            caption="" 
        )

    # ==========================================================
    # --- MOCKUP MONITORING PAGE ---
    # ==========================================================
    st.markdown('<div class="mockup-title" style="margin-top: 40px;">Monitoring Page</div>', unsafe_allow_html=True)
    
    # Render nilai-nilai monitoring yang sudah di-center
    col_left, col_center_mon, col_right = st.columns([1, 4, 1])
    
    with col_center_mon:
        # Menggunakan kolom di dalam kolom tengah untuk tata letak nilai
        col_mon1, col_mon2, col_mon3 = st.columns(3)
        
        kap_val = st.session_state.sensor_data["kapasitas"]
        suhu_val = st.session_state.sensor_data["suhu"]
        kelem_val = st.session_state.sensor_data["kelembapan"]
        
        with col_mon1:
            st.markdown('<div class="icon-title-mock">🗑️ Kapasitas Tempat Sampah (%)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box-mock" style="background-color: #FFB6C1; color: black; padding: 15px;">{kap_val}%</div>', unsafe_allow_html=True)
            
        with col_mon2:
            st.markdown('<div class="icon-title-mock">🌡️ Suhu (°C)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box-mock" style="background-color: #FF8C00; color: white;">{suhu_val}°C</div>', unsafe_allow_html=True) 
            
        with col_mon3:
            st.markdown('<div class="icon-title-mock">💧 Kelembapan (%)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box-mock" style="background-color: #FFD700; color: black; padding: 15px;">{kelem_val}%</div>', unsafe_allow_html=True) 

    # ==========================================================
    # --- MOCKUP RIWAYAT PAGE (TABEL DIPUSATKAN) ---
    # ==========================================================
    st.markdown('<div class="mockup-title" style="margin-top: 50px;">Riwayat Page</div>', unsafe_allow_html=True)

    # --- TABEL 1: Waktu & Kapasitas (DIPUSATKAN) ---
    render_centered_table(
        title_markdown='<div class="table-title-header"><span class="table-icon">⏰</span> Waktu <span class="table-icon">🗑️</span> Kapasitas (%)</div>',
        data_rows=mock_data_kapasitas,
        header_cells='<div class="table-header-cell">⏰ Waktu</div><div class="table-header-cell">🗑️ Kapasitas (%)</div>'
    )

    # --- TABEL 2: Suhu & Kelembapan (DIPUSATKAN) ---
    render_centered_table(
        title_markdown='<div class="table-title-header" style="margin-top: 25px;"><span class="table-icon">🌡️</span> Suhu (°C) <span class="table-icon">💧</span> Kelembapan (%)</div>',
        data_rows=mock_data_suhu,
        header_cells='<div class="table-header-cell">🌡️ Suhu (°C)</div><div class="table-header-cell">💧 Kelembapan (%)</div>'
    )
        
    
    # --- SECTION HOW IT WORKS ---
    st.markdown("<h2 style='margin-top: 50px;'>How it works?</h2>", unsafe_allow_html=True)
    st.markdown("""
        <ul class="how-it-works-list">
            <li><b>1. Hubungkan Perangkat IoT</b><br>Sambungkan sensor dengan WiFi dan sistem SmartBin</li>
            <li><b>2. Pantau dari Website</b><br>Login dan pantau status tempat sampah secara real-time</li>
            <li><b>3. Dapatkan Notifikasi</b><br>Terima peringatan ketika tempat sampah penuh dan suhu dari dalam tempat sampah</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("<p>Bersama kita wujudkan kebersihan berkelanjutan<br>Mulai langkah kecil untuk bumi yang lebih hijau</p>", unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("""
    <div class="footer-text">
        3 D4 Teknik Komputer A
        <br>
        @SmartBin
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_landing_page()