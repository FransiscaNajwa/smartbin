import streamlit as st
from Pages import homepage, landingpage, loginpage, monitpage, notifpage, profilpage, regispage, riwayatpage

# Konfigurasi halaman utama
st.set_page_config(page_title="SmartBin", page_icon="🗑️", layout="wide")

# Inisialisasi session state untuk navigasi
if "page" not in st.session_state:
    st.session_state.page = "Landing"

# CSS Kustom untuk desain konsisten
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #C3B1E1, #B0C4DE);
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
    .btn-logout, .btn-login, .btn-register {
        background-color: black;
        color: white;
        border-radius: 6px;
        padding: 6px 14px;
        text-decoration: none;
        font-weight: bold;
        margin-left: 10px;
    }
    .btn-login {
        background-color: white;
        color: black;
    }
    .footer {
        text-align: center;
        margin-top: 60px;
        font-style: italic;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h2>SmartBin</h2>
    <div class="nav">
        <a href="#" onclick='javascript:window.location.href = "/?page=Landing"'>Home</a>
        <a href="#" onclick='javascript:window.location.href = "/?page=Monitoring"'>Monitoring</a>
        <a href="#" onclick='javascript:window.location.href = "/?page=Riwayat"'>Riwayat</a>
        <a href="#" onclick='javascript:window.location.href = "/?page=Notifikasi"'>Notifikasi</a>
        <a href="#" onclick='javascript:window.location.href = "/?page=Profil"'>Profil</a>
        <a class="btn-logout" href="#" onclick='javascript:window.location.href = "/?page=Login"'>Logout</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Logika navigasi berdasarkan session state
page = st.session_state.page

if page == "Landing":
    landingpage.show()  # Panggil fungsi show dari landingpage.py
elif page == "Login":
    loginpage.show()   # Panggil fungsi show dari loginpage.py
elif page == "Register":
    regispage.show()   # Panggil fungsi show dari regispage.py
elif page == "Monitoring":
    monitpage.show()   # Panggil fungsi show dari monitpage.py
elif page == "Notifikasi":
    notifpage.show()   # Panggil fungsi show dari notifpage.py
elif page == "Profil":
    profilpage.show()  # Panggil fungsi show dari profilpage.py
elif page == "Riwayat":
    riwayatpage.show() # Panggil fungsi show dari riwayatpage.py
elif page == "Homepage":
    homepage.show()    # Panggil fungsi show dari homepage.py
else:
    st.write("Halaman tidak ditemukan. Pilih dari menu di atas.")

# Footer
st.markdown("""
<div class="footer">
    D4 Teknik Komputer A @SmartBin
</div>
""", unsafe_allow_html=True)

# Fungsi untuk mengubah halaman saat tombol diklik (opsional, bisa diganti dengan sidebar)
def change_page(new_page):
    st.session_state.page = new_page
    st.experimental_rerun()  # Refresh halaman

# Sidebar untuk navigasi alternatif (opsional)
st.sidebar.title("Navigasi")
if st.sidebar.button("Landing Page"):
    change_page("Landing")
if st.sidebar.button("Login"):
    change_page("Login")
if st.sidebar.button("Register"):
    change_page("Register")
if st.sidebar.button("Monitoring"):
    change_page("Monitoring")
if st.sidebar.button("Notifikasi"):
    change_page("Notifikasi")
if st.sidebar.button("Profil"):
    change_page("Profil")
if st.sidebar.button("Riwayat"):
    change_page("Riwayat")
if st.sidebar.button("Homepage"):
    change_page("Homepage")