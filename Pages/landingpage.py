import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="SmartBin", page_icon="🗑️", layout="wide")

# CSS kustom untuk gaya
st.markdown("""
    <style>
    body {
        background-color: #b3a6f2;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 40px;
        background-color: #b3a6f2;
    }
    .header h2 {
        color: black;
        font-weight: bold;
    }
    .nav a {
        margin-left: 20px;
        text-decoration: none;
        color: black;
        font-weight: 500;
    }
    .btn {
        background-color: black;
        color: white;
        border-radius: 6px;
        padding: 6px 14px;
        text-decoration: none;
        font-weight: bold;
    }
    .hero {
        text-align: center;
        padding: 40px;
    }
    .hero h1 {
        font-size: 40px;
        font-weight: 800;
    }
    .section-title {
        font-size: 28px;
        font-weight: bold;
        margin-top: 50px;
    }
    .center {
        text-align: center;
    }
    .how {
        font-style: italic;
        margin-top: 50px;
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h2>SmartBin</h2>
    <div class="nav">
        <a href="#">Home</a>
        <a href="#">Fitur</a>
        <a class="btn" href="#">Register</a>
        <a class="btn" style="background-color:white; color:black;" href="#">Login</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero">
    <h1>Welcome to SmartBin</h1>
    <p>Track, Monitor, and Stay Clean........</p>
</div>
""", unsafe_allow_html=True)

st.image("https://cdn.pixabay.com/photo/2017/09/06/19/05/garbage-2729601_1280.jpg", use_column_width=True)

# Fitur Section
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://www.shutterstock.com/shutterstock/photos/174287021/display_1500/stock-vector-trash-can-with-garbage-and-recycling-symbol-174287021.jpg")
    st.markdown("### Monitoring Real Time")
    st.caption("Pantau kapasitas, suhu, dan kelembapan tempat sampah secara real-time")
with col2:
    st.image("https://www.shutterstock.com/shutterstock/photos/174287021/display_1500/stock-vector-trash-can-with-garbage-and-recycling-symbol-174287021.jpg")
    st.markdown("### Notifikasi Otomatis")
    st.caption("Dapatkan peringatan saat tempat sampah hampir penuh")
with col3:
    st.image("https://www.shutterstock.com/shutterstock/photos/174287021/display_1500/stock-vector-trash-can-with-garbage-and-recycling-symbol-174287021.jpg")
    st.markdown("### Riwayat & Grafik")
    st.caption("Lihat tren kebersihan harian, mingguan, dan bulanan")

# Grafik Data
st.markdown("<div class='section-title center'>Grafik Data Riwayat</div>", unsafe_allow_html=True)
st.image("https://cdn.theguardian.com/environment/2020/mar/18/recycling-data.jpg", use_column_width=True)

# How it works
st.markdown("""
<div class="how">
<h3><em>How it works?</em></h3>
<b>1. Hubungkan Perangkat IoT</b><br>
Sambungkan sensor dengan WiFi dan sistem SmartBin<br><br>

<b>2. Pantau dari Website</b><br>
Login dan lihat status tempat sampah secara real-time<br><br>

<b>3. Dapatkan Notifikasi</b><br>
Terima peringatan ketika tempat sampah penuh dan suhu dari dalam tempat sampah<br><br>

<b>Bersama kita wujudkan kebersihan berkelanjutan<br>
Mulai langkah kecil untuk bumi yang lebih hijau 🌱</b><br><br>

<a class="btn" style="background-color:black;" href="#">Login</a>
<a class="btn" style="background-color:white; color:black;" href="#">Register Now!</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
3 D4 Teknik Komputer A<br>
@SmartBin
</div>
""", unsafe_allow_html=True)