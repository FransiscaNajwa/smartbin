import streamlit as st

# Bagian selamat datang (seperti di sisi kanan gambar)
st.markdown(
    """
    <style>
    .welcome {
        color: black;
        font-size: 36px;
        text-align: center;
        margin-top: 50px;
    }
    .slogan {
        color: black;
        font-size: 24px;
        text-align: center;
    }
    </style>
    <div class="welcome">Welcome to SmartBin</div>
    <div class="slogan">Track, Monitor, Stay Clean</div>
    """,
    unsafe_allow_html=True
)

# Judul dan desain halaman
st.title("Register")

# Formulir pendaftaran
with st.form(key="register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Konfirmasi Password", type="password")
    submit_button = st.form_submit_button(label="Submit")

    # Validasi sederhana
    if submit_button:
        if not username or not email or not password or not confirm_password:
            st.error("Harap isi semua kolom!")
        elif password != confirm_password:
            st.error("Password dan Konfirmasi Password tidak cocok!")
        else:
            st.success("Pendaftaran berhasil! Mengarahkan ke login...")
            # Di sini Anda bisa menambahkan logika untuk menyimpan data (misalnya ke database)

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