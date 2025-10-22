import streamlit as st
from PIL import Image
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="SmartBin",
    layout="wide",
)

# Path gambar
BASE_DIR = Path(__file__).resolve().parent
img_path = BASE_DIR / "assets" / "sampah.png"

# Warna
HEADER_COLOR = "#B0A8DC"
BACKGROUND_COLOR = "#AAB3EF"
CARD_COLOR = "#F9B97F"

# CSS kustom (perbaikan header & tabel)
st.markdown(f"""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"],
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"], .main {{
            background-color: {BACKGROUND_COLOR} !important;
            width: 100% !important;
            min-height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        [data-testid="stHeader"] {{
            background: none !important;
            height: 0px !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        /* HEADER */
        .custom-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 999;
            background-color: {HEADER_COLOR};
            border-radius: 0 0 20px 20px;
            padding: 10px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        }}
        .header-title {{
            font-size: 28px;
            font-weight: 700;
            color: black;
            letter-spacing: 1px;
        }}
        .header-buttons {{
            display: flex;
            gap: 15px;
        }}
        .header-buttons button {{
            background-color: white;
            color: black;
            border: none;
            padding: 6px 20px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .header-buttons button:hover {{
            background-color: #F0F0F0;
        }}

        /* MAIN SECTION */
        .content {{
            padding-top: 100px; /* agar konten tidak tertutup header */
            text-align: center;
        }}

        /* CARD INFO */
        .info-card {{
            background-color: {CARD_COLOR};
            border-radius: 15px;
            padding: 10px 25px;
            font-size: 40px;
            font-weight: 600;
            text-align: center;
            color: black;
            width: 50%;
            margin: 10px auto;
        }}

        .section-title {{
            font-size: 26px;
            font-weight: 700;
            margin-top: 50px;
            text-align: center;
        }}

        /* TABEL */
        [data-testid="stTable"] {{
            background-color: white !important;
            border-radius: 12px !important;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .italic {{
            font-style: italic;
            text-align: center;
            margin-top: 40px;
        }}

        .footer {{
            text-align: center;
            font-size: 14px;
            color: black;
            margin-top: 20px;
            padding-bottom: 30px;
        }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
    <div class="custom-header">
        <div class="header-title">SmartBin</div>
        <div class="header-buttons">
            <form action='LoginPage' method='get'>
                <button type='submit'>Login</button>
            </form>
            <form action='RegisterPage' method='get'>
                <button type='submit'>Register</button>
            </form>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.markdown("<div class='content'>", unsafe_allow_html=True)

st.markdown("<h3>Welcome to SmartBin</h3>", unsafe_allow_html=True)
st.markdown("<p>Track, Monitor, and Stay Clean...</p>", unsafe_allow_html=True)

# Gambar utama
try:
    image = Image.open(img_path)
    st.image(image, use_container_width=True)
except FileNotFoundError:
    st.error("❌ Gambar 'sampah.png' tidak ditemukan di folder assets/")

# --- MONITORING PAGE ---
st.markdown("<div class='section-title'>Monitoring Page</div>", unsafe_allow_html=True)
st.markdown("🗑️ **Kapasitas Tempat Sampah (%)**")
st.markdown("<div class='info-card'>68%</div>", unsafe_allow_html=True)
st.markdown("🌡️ **Suhu (°C)**")
st.markdown("<div class='info-card'>32°C</div>", unsafe_allow_html=True)
st.markdown("💧 **Kelembapan (%)**")
st.markdown("<div class='info-card'>60%</div>", unsafe_allow_html=True)

# --- RIWAYAT PAGE ---
st.markdown("<div class='section-title'>Riwayat Page</div>", unsafe_allow_html=True)
st.table({
    "🕓 Waktu": ["10:30", "10:45"],
    "🗑️ Kapasitas (%)": [65, 68]
})
st.table({
    "🌡️ Suhu (°C)": [31, 32],
    "💧 Kelembapan (%)": [58, 60]
})

# --- HOW IT WORKS ---
st.markdown("<div class='section-title'>How it works?</div>", unsafe_allow_html=True)
st.markdown("""
**1. Hubungkan Perangkat IoT**  
Sambungkan sensor dengan WiFi dan sistem SmartBin  

**2. Pantau dari Website**  
Login dan lihat status tempat sampah secara real-time  

**3. Dapatkan Notifikasi**  
Terima peringatan ketika tempat sampah penuh dan suhu dalam tempat sampah meningkat
""")

# --- FOOTER ---
st.markdown("""
<div class='italic'>
Bersama kita wujudkan kebersihan berkelanjutan  
Mulai langkah kecil untuk bumi yang lebih hijau
</div>
<div class='footer'>
    <b>3 D4 Teknik Komputer A</b><br>
    @SmartBin
</div>
</div>
""", unsafe_allow_html=True)
