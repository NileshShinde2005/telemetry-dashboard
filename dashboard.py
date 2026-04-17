import streamlit as st
import pandas as pd
import random
import time
import os
from datetime import datetime

st.set_page_config(page_title="🛰️ Aerospace Telemetry", layout="wide")

# ---------- TITLE ----------
st.title("🛰️ Aerospace Telemetry Dashboard")
st.caption("Real-time telemetry simulation (Cloud Version)")

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

# calculate delta
delta_alt = altitude - df["Altitude"].iloc[-2] if len(df) > 1 else 0
delta_speed = speed - df["Speed"].iloc[-2] if len(df) > 1 else 0
delta_temp = temperature - df["Temperature"].iloc[-2] if len(df) > 1 else 0

col1.metric("📡 Altitude (ft)", altitude, delta_alt)
col2.metric("🚀 Speed (km/h)", speed, delta_speed)
col3.metric("🌡️ Temperature (°C)", temperature, delta_temp)

st.divider()

# ---------- GRAPHS ----------
st.markdown("### 📈 Graphs (Last 30 Readings)")

chart_df = df.tail(30)

st.subheader("📡 Altitude")
st.line_chart(chart_df["Altitude"])

st.subheader("🚀 Speed")
st.line_chart(chart_df["Speed"])

st.subheader("🌡️ Temperature")
st.line_chart(chart_df["Temperature"])

st.divider()

# ---------- IMAGE SECTION ----------
st.markdown("### 📷 Latest Captured Images")

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
    col1.image(os.path.join(image_folder, images[0]), use_column_width=True)
    if len(images) > 1:
        col2.image(os.path.join(image_folder, images[1]), use_column_width=True)

# ---------- AUTO REFRESH ----------
time.sleep(1)
st.rerun()
