import streamlit as st
from app.streamlit_app.LandingPage import show_landing_page
from app.streamlit_app.LoginPage import show_login_page
from app.streamlit_app.RegisterPage import show_register_page
from app.streamlit_app.HomePage import show_home_page

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "LandingPage"

page = st.session_state["current_page"]

if page == "LandingPage":
    show_landing_page()
elif page == "LoginPage":
    show_login_page()
elif page == "RegisterPage":
    show_register_page()
elif page == "HomePage":
    show_home_page()
