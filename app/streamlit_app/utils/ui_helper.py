# streamlit_app/utils/ui_helper.py
import streamlit as st
from pathlib import Path

def load_css(file_path: str):
    css_path = Path(__file__).resolve().parent.parent / "assets" / file_path
    if not css_path.exists():
        st.warning(f"⚠️ CSS file tidak ditemukan: {css_path}")
        return
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)