import streamlit as st

def go_to_page(page_name: str):
    """
    Navigasi antar halaman Streamlit menggunakan session_state.
    Halaman tujuan harus terdaftar di main.py atau sidebar.
    """
    # Inisialisasi halaman default jika belum ada
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "LoginPage"
    
    # Ganti halaman ke yang dituju
    st.session_state["current_page"] = page_name

    # Jalankan ulang Streamlit agar halaman berpindah
    st.rerun()


def logout():
    """
    Logout user dan arahkan ke halaman login.
    """
    # Hapus data user dari session_state
    st.session_state.pop("user", None)
    
    # Kembali ke halaman login
    st.session_state["current_page"] = "LoginPage"
    
    # Jalankan ulang Streamlit agar halaman berubah
    st.rerun()
