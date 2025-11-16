import streamlit as st
import time
from app.utils.ui_helper import load_css
from app.database.user_crud import verify_user

def show_login_page(go_to):
    load_css("style.css")

    # Cek apakah sudah login
    if "user" in st.session_state and st.session_state["user"]:
        st.success(f"👋 Kamu sudah login sebagai @{st.session_state['user']['username']}")
        if st.button("Lanjut ke Home", use_container_width=True):
            go_to("HomePage")
        return

    # Header
    st.markdown("""
        <div class="centered-text">
            <h1>Selamat Datang di SmartBin</h1>
        </div>
    """, unsafe_allow_html=True)

    # Form login
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.subheader("Form Masuk")
        email = st.text_input("Email", placeholder="Masukkan email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        submitted = st.form_submit_button("Masuk")

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

    # Navigasi tambahan untuk register
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)
    nav_col, _ = st.columns([1, 3])
    with nav_col:
        st.markdown("<p class='small-note'>Belum punya akun?</p>", unsafe_allow_html=True)
        if st.button("Daftar"):
            go_to("RegisterPage")
    st.markdown("</div>", unsafe_allow_html=True)