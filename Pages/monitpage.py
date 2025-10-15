import streamlit as st

# Judul dan navigasi
st.write("SmartBin")
st.button("Home")

# Bagian Kapasitas Tempat Sampah
with st.container():
    st.markdown("<h3 style='text-align: center;'>Kapasitas Tempat Sampah (%)</h3>", unsafe_allow_html=True)
    st.progress(0.3)  # Simulasi 30% kapasitas
    st.button("Reset Status")

# Bagian Suhu
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("🌡️ Suhu (°C)")
    with col2:
        st.markdown(
            """
            <style>
            .temp-box {
                background-color: #f4a261;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                color: black;
                font-size: 24px;
                margin: 5px;
            }
            .temp-text {
                font-size: 14px;
                color: black;
            }
            </style>
            <div class="temp-box">32°C</div>
            <div class="temp-text">Tiga puluh dua derajat</div>
            """,
            unsafe_allow_html=True
        )
    st.button("Alert")

# Bagian Kelembapan
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("💧 Kelembapan (%)")
    with col2:
        st.markdown(
            """
            <style>
            .temp-box {
                background-color: #f4a261;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                color: black;
                font-size: 24px;
                margin: 5px;
            }
            .temp-text {
                font-size: 14px;
                color: black;
            }
            </style>
            <div class="temp-box">32°C</div>
            <div class="temp-text">Tiga puluh dua derajat</div>
            """,
            unsafe_allow_html=True
        )
    st.button("Alert")

# Bagian Status Umum
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("⚠️ Status Umum (Aman / Hampir Penuh / Penuh)")
    with col2:
        st.markdown(
            """
            <style>
            .status-box {
                background-color: #f4a261;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                color: black;
                font-size: 24px;
                margin: 5px;
            }
            .status-text {
                font-size: 14px;
                color: black;
            }
            </style>
            <div class="status-box">Aman</div>
            <div class="status-text">Tempat sampah dalam keadaan aman</div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.write("D4 Teknik Komputer A @SmartBin")

# Warna latar belakang menyerupai gambar
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #C3B1E1, #B0C4DE);
    }
    </style>
    """,
    unsafe_allow_html=True
)