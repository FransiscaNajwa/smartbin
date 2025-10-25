import streamlit as st
from streamlit_app.utils.ui_helper import load_css
from app.database.crud_operations import register_user, get_user_by_email

def show_register_page(go_to):
    load_css("style.css")

    # Header
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to Register Page</h1>
        </div>
    """, unsafe_allow_html=True)

    # Form registrasi
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("register_form"):
        st.subheader("Register Form")
        username = st.text_input("Username", placeholder="Buat username")
        email = st.text_input("Email", placeholder="Masukkan email baru")
        password = st.text_input("Password", type="password", placeholder="Buat password")
        confirm = st.text_input("Konfirmasi Password", type="password", placeholder="Ulangi password")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Validasi input
            if not username or not email or not password or not confirm:
                st.warning("⚠️ Semua field harus diisi.")
            elif password != confirm:
                st.error("❌ Password dan konfirmasi tidak cocok.")
            elif get_user_by_email(email):
                st.error("❌ Email sudah terdaftar.")
            else:
                user_id = register_user(username, password, email)
                st.success("✅ Registrasi berhasil! Silakan login.")
                st.balloons()
                go_to("LoginPage")

    st.markdown("</div>", unsafe_allow_html=True)

    # Navigasi kembali
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        go_to("LandingPage")
    st.markdown("</div>", unsafe_allow_html=True)