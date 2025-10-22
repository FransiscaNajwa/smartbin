import streamlit as st

def set_page_config(title: str, icon: str):
    st.set_page_config(page_title=title, page_icon=icon, layout="centered")
