import streamlit as st
import time
from streamlit_app.utils.ui_helper import load_css
from app.database.crud_operations import get_user_by_email, get_user_by_id, hash_password
from app.database.mongo_client import db

def show_profile_page(go_to=None):
    load_css("style.css")

    # Ambil user dari session
    user = st.session_state.get("user")
    if not user:
        st.error("⚠️ Anda belum login.")
        if go_to:
            go_to("LoginPage")
        return

    # Ambil data user terbaru dari DB
    user_data = get_user_by_id(user["_id"])
    if not user_data:
        st.error("❌ Gagal mengambil data profil.")
        return

    # Simpan ke session_state.profile_data
    st.session_state.profile_data = {
        "email": user_data["email"],
        "username": user_data["username"]
    }

    # Title
    st.markdown("<h1 class='centered-text'>Welcome to Profile Page</h1>", unsafe_allow_html=True)

    # Profile Card
    profile = st.session_state.profile_data
    st.markdown(f"""
        <div class='profile-card' style='margin-left: 50px;'>
            <div class='profile-info'>
                <p><strong>Email:</strong> {profile['email']}</p>
                <p><strong>Username:</strong> {profile['username']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Form Edit Profile
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)

    with st.form("profile_form"):
        st.subheader("Edit Profile")
        email = st.text_input("Email", value=profile["email"], placeholder="Masukkan email baru")
        username = st.text_input("Username", value=profile["username"], placeholder="Masukkan username baru")
        password = st.text_input("Password", placeholder="Masukkan password baru", type="password")
        submitted = st.form_submit_button("Save")

        if submitted:
            if not username or not email:
                st.error("❌ Email dan Username wajib diisi.")
            else:
                with st.spinner("Menyimpan profil..."):
                    update_fields = {
                        "email": email,
                        "username": username
                    }
                    if password:
                        update_fields["password"] = hash_password(password)

                    result = db.users.update_one(
                        {"_id": user["_id"]},
                        {"$set": update_fields}
                    )

                    if result.modified_count > 0:
                        st.session_state.profile_data = {
                            "email": email,
                            "username": username
                        }
                        st.session_state.user["email"] = email
                        st.session_state.user["username"] = username
                        st.success("✅ Profil berhasil diperbarui.")
                    else:
                        st.info("ℹ️ Tidak ada perubahan yang disimpan.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Tombol Back
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