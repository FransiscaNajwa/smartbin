import streamlit as st
from streamlit_app.utils.ui_helper import load_css

def show_register_page(go_to):
    load_css("style.css")

    # Header teks
    st.markdown("""
        <div class="centered-text">
            <h1>Welcome to SmartBin</h1>
            <h3>Track, Monitor, Stay Clean</h3>
        </div>
    """, unsafe_allow_html=True)

    # Form registrasi dalam kotak
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("register_form"):
        st.subheader("Register")
        username = st.text_input("Username", placeholder="Buat username")
        email = st.text_input("Email", placeholder="Masukkan email baru")
        password = st.text_input("Password", type="password", placeholder="Buat password")  # ✅ tanpa koma
        confirm = st.text_input("Konfirmasi Password", type="password", placeholder="Ulangi password")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not username or not email or not password or not confirm:
                st.warning("⚠️ Semua field harus diisi.")
            elif password != confirm:
                st.error("❌ Password tidak cocok.")
            else:
                st.success("✅ Registrasi berhasil! Silakan login.")
                go_to("LoginPage")

    st.markdown("</div>", unsafe_allow_html=True)  # ✅ Tutup form-box

    # Tombol navigasi di luar form-box
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    if st.button("⬅️ Back"):
        go_to("LandingPage")

    st.markdown("</div>", unsafe_allow_html=True)