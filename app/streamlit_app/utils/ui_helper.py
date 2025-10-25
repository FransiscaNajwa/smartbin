# streamlit_app/utils/ui_helper.py

import streamlit as st
from pathlib import Path

def load_css(file_name: str):
    """
    Memuat file CSS dari folder assets dan inject ke halaman Streamlit.
    """
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    css_path = assets_dir / file_name

    if not css_path.is_file():
        st.warning(f"⚠️ CSS file tidak ditemukan: {css_path.name}")
        return

    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Gagal memuat CSS: {e}")