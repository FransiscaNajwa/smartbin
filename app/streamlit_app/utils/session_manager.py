import streamlit as st

def go_to_page(page_name: str):
    """
    Navigasi antar halaman Streamlit menggunakan session_state.
    Halaman harus diatur secara manual di main.py atau sidebar.
    """
    st.session_state["current_page"] = page_name
    st.experimental_rerun()

def logout():
    """
    Hapus sesi pengguna dan arahkan ke halaman login.
    """
    st.session_state.pop("user", None)
    st.session_state["current_page"] = "LoginPage"
    st.experimental_rerun()