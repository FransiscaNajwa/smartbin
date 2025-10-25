import streamlit as st

def render_device_card(device_id, kapasitas, suhu, kelembapan, status):
    st.markdown(f"### 🗑️ SmartBin: `{device_id}`")
    st.metric("Kapasitas", f"{kapasitas}%")
    st.metric("Suhu", f"{suhu}°C")
    st.metric("Kelembapan", f"{kelembapan}%")
    st.success(f"Status: {status}")