import streamlit as st
import time
from streamlit_app.utils.ui_helper import load_css
from app.database.crud_operations import verify_user

def show_login_page(go_to):
    load_css("style.css")

    # Cek apakah sudah login
    if "user" in st.session_state:
        st.success(f"👋 Kamu sudah login sebagai {st.session_state.user['username']}")
        if st.button("Lanjut ke Home"):
            go_to("HomePage")
        return

    # Header
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to Login Page</h1>
        </div>
    """, unsafe_allow_html=True)

    # Form login
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.subheader("Login Form")
        email = st.text_input("Email", placeholder="Masukkan email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("❌ Email dan password harus diisi.")
            else:
                with st.spinner("Authenticating..."):
                    time.sleep(1)
                    user = verify_user(email, password)

                if user:
                    st.success(f"✅ Selamat datang, {user['username']}!")
                    st.session_state.user = user
                    go_to("HomePage")
                else:
                    st.error("❌ Email atau password salah.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Navigasi tambahan untuk register dan kembali ke landing
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)
    nav_col, _ = st.columns([1, 3])
    with nav_col:
        st.markdown("<p class='small-note'>Belum punya akun?</p>", unsafe_allow_html=True)
        if st.button("Register"):
            go_to("RegisterPage")
        if st.button("⬅️ Back"):
            go_to("LandingPage")
    st.markdown("</div>", unsafe_allow_html=True)