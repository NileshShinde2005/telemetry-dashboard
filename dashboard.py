import streamlit as st
import pandas as pd
import random
import time
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="🛰️ Aerospace Telemetry", layout="wide")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.05);
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🛰️ Aerospace Telemetry Dashboard")
st.caption("Real-time telemetry simulation (Cloud Version)")
st.info("Simulated telemetry system demonstrating satellite-to-ground data monitoring and visualization.")

st.divider()

# ---------- SESSION DATA ----------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Time", "Altitude", "Speed", "Temperature"])

df = st.session_state.df

# ---------- GENERATE DATA ----------
altitude = random.randint(1000, 5000)
speed = random.randint(200, 900)
temperature = random.randint(10, 50)

new_row = {
    "Time": datetime.now().strftime("%H:%M:%S"),
    "Altitude": altitude,
    "Speed": speed,
    "Temperature": temperature
}

df.loc[len(df)] = new_row
st.session_state.df = df

# ---------- METRICS ----------
st.markdown("### 🔍 Real-time Readings")

col1, col2, col3 = st.columns(3)

delta_alt = altitude - df["Altitude"].iloc[-2] if len(df) > 1 else 0
delta_speed = speed - df["Speed"].iloc[-2] if len(df) > 1 else 0
delta_temp = temperature - df["Temperature"].iloc[-2] if len(df) > 1 else 0

col1.metric("📡 Altitude", f"{altitude} ft", delta_alt)
col2.metric("🚀 Speed", f"{speed} km/h", delta_speed)
col3.metric("🌡️ Temperature", f"{temperature} °C", delta_temp)

st.divider()

# ---------- GRAPHS ----------
st.markdown("### 📈 Telemetry Trends")

chart_df = df.tail(30)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Altitude")
    fig1 = px.line(chart_df, y="Altitude", title="Altitude Trend", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Temperature")
    fig2 = px.line(chart_df, y="Temperature", title="Temperature Trend", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Speed")
    fig3 = px.line(chart_df, y="Speed", title="Speed Trend", template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---------- IMAGE SECTION ----------
st.markdown("### 📷 Satellite Camera Feed")
st.caption("Simulated onboard camera captures")

image_folder = "sample_images"
os.makedirs(image_folder, exist_ok=True)

# create sample images if empty
if len(os.listdir(image_folder)) == 0:
    from PIL import Image
    for i in range(3):
        img = Image.new('RGB', (400, 300), color=(
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        ))
        img.save(f"{image_folder}/img_{i}.jpg")

images = sorted(os.listdir(image_folder), reverse=True)[:2]

if images:
    col1, col2 = st.columns(2)
    col1.image(os.path.join(image_folder, images[0]), use_container_width=True)
    if len(images) > 1:
        col2.image(os.path.join(image_folder, images[1]), use_container_width=True)

# ---------- AUTO REFRESH ----------
time.sleep(1)
st.rerun()
