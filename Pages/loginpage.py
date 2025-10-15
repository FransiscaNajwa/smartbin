import streamlit as st

# Bagian selamat datang (ditempatkan di atas login)
st.markdown(
    """
    <style>
    .welcome {
        color: black;
        font-size: 36px;
        text-align: center;
        margin-top: 20px;
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
st.title("Login")

# Form login
with st.form(key="login_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button(label="Login")

    # Logika sederhana untuk login (hanya contoh)
    if submit_button:
        if username and email and password:
            st.success("Login berhasil! Mengarahkan ke dashboard...")
            # Di sini Anda bisa menambahkan logika untuk masuk ke halaman berikutnya
        else:
            st.error("Harap isi semua kolom!")

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