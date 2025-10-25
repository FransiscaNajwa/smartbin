import streamlit as st
import time
from streamlit_app.utils.ui_helper import load_css

def show_login_page(go_to):
    load_css("style.css")

    # Header teks
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to Login Page</h1>
        </div>
    """, unsafe_allow_html=True)

    # Form login dalam kotak
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.subheader("Login Form")
        username = st.text_input("Username", placeholder="Masukkan username")
        email = st.text_input("Email", placeholder="Masukkan email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not email or not password:
                st.error("❌ Semua field harus diisi.")
            else:
                with st.spinner("Authenticating..."):
                    time.sleep(1)
                st.success("✅ Login berhasil!")
                go_to("HomePage")

    st.markdown("</div>", unsafe_allow_html=True)  # ✅ Tutup form-box setelah form

    # Navigasi di luar form-box agar tidak tercampur
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    nav_col, _ = st.columns([1, 3])
    with nav_col:
        st.markdown("<p class='small-note'>Belum punya akun?</p>", unsafe_allow_html=True)
        if st.button("Register"):
            go_to("RegisterPage")
        if st.button("⬅️ Back"):
            go_to("LandingPage")

    st.markdown("</div>", unsafe_allow_html=True)