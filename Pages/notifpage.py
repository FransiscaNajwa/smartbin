import streamlit as st

# Judul dan navigasi
st.write("SmartBin")
st.button("Home")

# Ikon notifikasi dan tombol Clear
col1, col2 = st.columns([1, 1])
with col1:
    st.write("🔔")
with col2:
    st.button("Clear")

# Dropdown untuk kategori
selected_category = st.selectbox("Semua", ["Semua", "Kapasitas Sampah", "Suhu & Kelembapan"], index=0)

# Kategori Kapasitas Sampah
if selected_category in ["Semua", "Kapasitas Sampah"]:
    with st.container():
        st.markdown("<h3 style='text-align: center; background-color: #ff9999; padding: 10px; border-radius: 10px;'>🔔 Kategori: Kapasitas Sampah</h3>", unsafe_allow_html=True)
        st.write("1. Tempat sampah hampir penuh (80%)")
        st.write("   - Waktu: 05 Okt 2025, 10:45 WIB")
        st.write("   - Pesan: 'Tempat sampah di ruang rapat hampir penuh. Segera lakukan pengosongan sebelum meluap.'")
        st.write("2. Tempat sampah penuh (100%)")
        st.write("   - Waktu: 05 Okt 2025, 18:22 WIB")
        st.write("   - Pesan: 'Tempat sampah sudah penuh. Mohon kosongkan sekaran.'")

# Kategori Suhu & Kelembapan
if selected_category in ["Semua", "Suhu & Kelembapan"]:
    with st.container():
        st.markdown("<h3 style='text-align: center; background-color: #ff9999; padding: 10px; border-radius: 10px;'>🔔 Kategori: Suhu & Kelembapan</h3>", unsafe_allow_html=True)
        st.write("1. Suhu meningkat/diatas ambang batas (35°C)")
        st.write("   - Waktu: 04 Okt 2025, 13:15 WIB")
        st.write("   - Pesan: 'Suhu di dalam tempat sampah terlalu tinggi. Kemungkinan sampah organik mulai membusuk.'")
        st.write("2. Kelembapan terlalu tinggi (85%)")
        st.write("   - Waktu: 03 Okt 2025, 09:20 WIB")
        st.write("   - Pesan: 'Kelembapan di dalam tempat sampah meningkat. Periksa kondisi tutup atau kantong sampah.'")

# Footer
st.write("D4 Teknik Komputer A @SmartBin")

# Warna latar belakang menyerupai gambar
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #C3B1E1, #B0C4DE);
    }
    .stSelectbox {
        background-color: #ffe6e6;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)