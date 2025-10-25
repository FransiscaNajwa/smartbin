import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from streamlit_app.utils.ui_helper import load_css

# Konfigurasi halaman
st.set_page_config(page_title="SmartBin", layout="wide")

# Load CSS global dari folder assets
load_css("style.css")  # otomatis mencari di streamlit_app/assets/style.css

# Inisialisasi session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "LandingPage"

# Fungsi navigasi universal
def go_to(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

# Import semua halaman
from streamlit_app.LandingPage import show_landing_page
from streamlit_app.LoginPage import show_login_page
from streamlit_app.RegisterPage import show_register_page
from streamlit_app.HomePage import show_home_page
from streamlit_app.ProfilePage import show_profile_page
from streamlit_app.NotifikasiPage import show_notifikasi_page

# Routing halaman
page = st.session_state["current_page"]

if page == "LandingPage":
    show_landing_page(go_to)
elif page == "LoginPage":
    show_login_page(go_to)
elif page == "RegisterPage":
    show_register_page(go_to)
elif page == "HomePage":
    show_home_page(go_to)
elif page == "ProfilePage":
    show_profile_page(go_to)
elif page == "NotifikasiPage":
    show_notifikasi_page(go_to)
else:
    st.error(f"❌ Halaman '{page}' tidak ditemukan.")