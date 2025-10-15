import streamlit as st

# Judul dan navigasi
st.write("SmartBin")
st.button("Home")

# Filter dan tanggal
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("Pilih Rentang Waktu")
with col2:
    st.button("Tanggal")
with col3:
    st.button("Filter")

# Rata-rata kapasitas
st.markdown("<h3 style='text-align: center;'>Rata-rata kapasitas sampah per hari selama 7 hari terakhir</h3>", unsafe_allow_html=True)
st.progress(0.4)  # Simulasi 40% kapasitas

# Rata-rata suhu & kelembapan
st.markdown("<h3 style='text-align: center;'>Rata-rata suhu & kelembapan selama 7 hari terakhir</h3>", unsafe_allow_html=True)
st.progress(0.3)  # Simulasi 30% kapasitas

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

# Log
st.markdown("<h3 style='text-align: center;'>Log</h3>", unsafe_allow_html=True)
st.write("17/10/2025")
st.write("   - [10:20] Tempat sampah penuh")
st.write("   - [08:45] Kantong diganti")
st.write("   - [Kemarin] Suhu di atas batas normal")

# Footer
st.write("D4 Teknik Komputer A @SmartBin")

# Warna latar belakang menyerupai gambar
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