import streamlit as st
import pymongo
import json
import altair as alt 
import pandas as pd
from datetime import datetime, timedelta
import time
import numpy as np 

# --- KONEKSI MONGODB & MQTT (DINONAKTIFKAN UNTUK UI) ---
# Mock data state
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {"kapasitas": 68, "suhu": 32, "kelembapan": 75, "status": "Aman"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True 

# Fungsi navigasi sederhana
def navigate_to(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()
    
# Fungsi get color berdasarkan status
def get_status_color(status):
    if status == "Aman" or status == "Normal":
        return "#FF8C00" 
    elif status == "Hampir Penuh" or status == "Tinggi":
        return "#FFD700" 
    elif status == "Penuh" or status == "Bahaya":
        return "#FF4500" 
    return "#FF8C00"

# --- CONFIG & STYLING SESUAI DESAIN ---
st.set_page_config(page_title="SmartBin Monitoring", page_icon="🗑️", layout="wide")

st.markdown("""
    <style>
    /* 1. Latar Belakang: Ungu Muda Solid */
    .stApp {
        background-color: #C3B0E1; 
        background: #C3B0E1; 
        color: black;
        font-family: 'Arial', sans-serif;
    }
    
    /* 2. Styling Tombol Header */
    .stButton button {
        background-color: black;
        color: white;
        border-radius: 5px;
        padding: 8px 15px;
        width: auto;
        white-space: nowrap;
    }
    
    /* 3. PENTING: MENAMBAH MARGIN KIRI PADA SMARTBIN */
    .header-text {
        font-weight: bold; 
        font-size: 1.2em;
        margin-top: 0;
        margin-bottom: 0;
        /* Tambahkan margin kiri untuk mensejajarkan dengan konten di kolom tengah */
        padding-left: 10px; 
    }
    
    /* 4. Styling Kotak Nilai Suhu/Kelembaban/Status */
    .value-box {
        display: inline-block;
        border-radius: 10px;
        padding: 10px 15px;
        font-size: 2.5em; 
        font-weight: bold;
        text-align: center;
        margin-right: 20px;
        color: black; 
    }
    
    /* 5. Icon/Title Alignment */
    .card-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    
    /* 6. Footer Styling dan Separator */
    .footer-text {
        margin-top: 40px;
        font-style: italic;
        color: black;
    }
    .section-separator {
        margin: 25px 0; 
    }
    
    /* PENTING: Penyesuaian untuk alignment visual di kolom tengah */
    div[data-testid^="stHorizontalBlock"] > div > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    div[data-testid^="stHorizontalBlock"] .card-title {
        align-self: flex-start; 
        text-align: left;
    }
    
    </style>
""", unsafe_allow_html=True)


def show():
    # --- HEADER (SmartBin Kiri, Home Kanan) ---
    # Mempertahankan st.columns([1, 0.15])
    header_col1, header_col2 = st.columns([1, 0.15]) 
    
    with header_col1:
        # PENTING: Menambahkan div wrapper untuk menyelaraskan dengan kolom tengah
        st.markdown('<div style="display: flex; justify-content: flex-start;">'
                    '<div class="header-text">SmartBin</div>'
                    '</div>', unsafe_allow_html=True)

    with header_col2:
        if st.button("Home", key="home_button"): 
            navigate_to("Homepage")

    # Ambil data dari session state
    latest_data = st.session_state.sensor_data
    
    # Rasio kolom untuk konten tengah
    CONTENT_COLS = [1.5, 3, 1.5]

    # ==========================================================
    # --- 1. KAPASITAS TEMPAT SAMPAH ---
    # ==========================================================
    st.markdown('<div class="section-separator">', unsafe_allow_html=True)
    with st.container():
        
        capacity_value = latest_data['kapasitas']
        capacity_color = "#F8BBD0" 
        
        col_left, col_center, col_right = st.columns(CONTENT_COLS)

        with col_center:
            # Judul Kapasitas
            st.markdown('<div class="card-title">🗑️ Kapasitas Tempat Sampah (%)</div>', unsafe_allow_html=True)

            # Nilai Kapasitas
            st.markdown(f'<div class="value-box" style="background-color: {capacity_color};">{capacity_value}%</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==========================================================
    # --- 2. SUHU (°C) ---
    # ==========================================================
    st.markdown('<div class="section-separator">', unsafe_allow_html=True)
    with st.container():
        
        suhu_val = latest_data['suhu']
        suhu_color = "#F8BBD0" 
        
        col_left, col_center, col_right = st.columns(CONTENT_COLS)
        
        with col_center:
            st.markdown('<div class="card-title">🌡️ Suhu (°C)</div>', unsafe_allow_html=True)

            # Nilai Suhu
            st.markdown(f'<div class="value-box" style="background-color: {suhu_color};">{suhu_val}°C</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    # --- 3. KELEMBAPAN (%) ---
    # ==========================================================
    st.markdown('<div class="section-separator">', unsafe_allow_html=True)
    with st.container():
        
        kelembapan_val = latest_data['kelembapan']
        kelembapan_color = "#FFD700" 
        
        col_left, col_center, col_right = st.columns(CONTENT_COLS)

        with col_center:
            st.markdown('<div class="card-title">💧 Kelembapan (%)</div>', unsafe_allow_html=True)

            # Nilai Kelembapan
            st.markdown(f'<div class="value-box" style="background-color: {kelembapan_color};">{kelembapan_val}%</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    # --- 4. STATUS UMUM ---
    # ==========================================================
    st.markdown('<div class="section-separator">', unsafe_allow_html=True)
    with st.container():
        
        status_umum = latest_data['status']
        status_color = get_status_color(status_umum)
        
        col_left, col_center, col_right = st.columns(CONTENT_COLS)

        with col_center:
            st.markdown('<div class="card-title">⚠️ Status Umum (Aman / Hampir Penuh / Penuh)</div>', unsafe_allow_html=True)

            # Nilai Status
            st.markdown(f'<div class="value-box" style="background-color: {status_color}; color: white;">{status_umum}</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)


    # --- FOOTER ---
    st.markdown("""
        <div class="footer-text">
        3 D4 Teknik Komputer A
        <br>
        @SmartBin
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()