import streamlit as st
import time
from streamlit_app.utils.ui_helper import load_css

def show_profile_page(go_to=None):
    load_css("style.css")

    # State untuk menyimpan data profil (hanya email dan username)
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = None  # Belum ada data tersimpan

    # Title
    st.markdown("<h1 class='centered-text'>Welcome to Profile Page</h1>", unsafe_allow_html=True)

    # Profile Card (hanya tampil jika sudah disimpan)
    if st.session_state.profile_data:
        profile = st.session_state.profile_data
        st.markdown(f"""
            <div class='profile-card' style='margin-left: 50px;'>
                <div class='profile-info'>
                    <p><strong>Email:</strong> {profile['email']}</p>
                    <p><strong>Username:</strong> {profile['username']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Form profile dalam kotak
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("profile_form"):
        st.subheader("Edit Profile")
        email = st.text_input("Email", value="", placeholder="Masukkan email baru")
        username = st.text_input("Username", value="", placeholder="Masukkan username baru")
        password = st.text_input("Password", placeholder="Masukkan password baru", type="password")
        submitted = st.form_submit_button("Save")

        if submitted:
            if not username or not email:
                st.error("❌ Email dan Username wajib diisi.")
            else:
                with st.spinner("Menyimpan profil..."):
                    time.sleep(1)
                st.session_state.profile_data = {
                    "email": email,
                    "username": username
                }
                st.success("✅ Profil berhasil disimpan.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Tombol Back ke HomePage
    if st.button("⬅️ Back"):
        if go_to:
            go_to("HomePage")

    # Footer
    st.markdown("""
    <div class='footer'>
        <b>3 D4 Teknik Komputer A</b><br>
        <b>@SmartBin</b>
    </div>
    """, unsafe_allow_html=True)