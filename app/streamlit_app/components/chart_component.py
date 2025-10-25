import streamlit as st
import pandas as pd
import altair as alt

def render_chart(df, sensor_type):
    chart = alt.Chart(df).mark_line().encode(
        x='timestamp:T',
        y='value:Q',
        tooltip=['timestamp', 'value']
    ).properties(title=f"Grafik {sensor_type.capitalize()}")
    st.altair_chart(chart, use_container_width=True)