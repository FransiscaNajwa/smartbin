import os
import streamlit as st


def go_to_page(page_name: str):
    """
    Navigasi antar halaman Streamlit (satu file per halaman).

    Contoh:
        go_to_page("LandingPage")  -> buka LandingPage.py
        go_to_page("RegisterPage") -> buka RegisterPage.py
    """
    # Pastikan nama page tanpa ekstensi .py
    if page_name.endswith(".py"):
        page_name = page_name.replace(".py", "")

    # Path absolut ke file tujuan
    app_dir = os.path.dirname(__file__)
    target_path = os.path.abspath(os.path.join(app_dir, f"../{page_name}.py"))

    # Cek apakah file ada, lalu pindahkan halaman
    if os.path.exists(target_path):
        st.session_state["current_page"] = page_name
        st.switch_page(f"app/streamlit_app/{page_name}.py")
    else:
        st.error(f"❌ Halaman '{page_name}' tidak ditemukan! Pastikan file ada di 'streamlit_app/'.")


def logout():
    """
    Hapus sesi pengguna dan kembali ke halaman login.
    """
    if "user" in st.session_state:
        del st.session_state["user"]

    st.switch_page("app/streamlit_app/LoginPage.py")
