import streamlit as st
import pandas as pd
import random
import time
import os
from datetime import datetime

st.set_page_config(page_title="🛰️ Aerospace Telemetry", layout="wide")

# folder for images
image_folder = "sample_images"
os.makedirs(image_folder, exist_ok=True)

# create dummy images if empty (optional)
if len(os.listdir(image_folder)) == 0:
    from PIL import Image
    for i in range(3):
        img = Image.new('RGB', (400, 300), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        img.save(f"{image_folder}/img_{i}.jpg")

# session state dataframe
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Time", "Altitude", "Speed", "Temperature"])

st.title("🛰️ Aerospace Telemetry Dashboard")
st.markdown("Simulated real-time aircraft telemetry system.")

placeholder_metrics = st.empty()
placeholder_graphs = st.empty()
placeholder_images = st.empty()

# loop simulation
for i in range(1000):

    altitude = random.randint(1000, 5000)
    speed = random.randint(200, 900)
    temperature = random.randint(10, 50)

    new_row = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Altitude": altitude,
        "Speed": speed,
        "Temperature": temperature
    }

    st.session_state.df.loc[len(st.session_state.df)] = new_row

    df = st.session_state.df

    # -------- METRICS --------
    with placeholder_metrics.container():
        st.markdown("### 🔍 Real-time Readings")
        col1, col2, col3 = st.columns(3)
        col1.metric("📡 Altitude (ft)", altitude)
        col2.metric("🚀 Speed (km/h)", speed)
        col3.metric("🌡️ Temperature (°C)", temperature)

    # -------- GRAPHS --------
    with placeholder_graphs.container():
        st.markdown("### 📈 Graphs (Last 30 Readings)")
        chart_df = df.tail(30)

        st.subheader("📡 Altitude")
        st.line_chart(chart_df["Altitude"])

        st.subheader("🚀 Speed")
        st.line_chart(chart_df["Speed"])

        st.subheader("🌡️ Temperature")
        st.line_chart(chart_df["Temperature"])

    # -------- IMAGES --------
    with placeholder_images.container():
        st.markdown("### 📷 Latest Captured Images")
        images = sorted(os.listdir(image_folder), reverse=True)[:2]

        if images:
            col1, col2 = st.columns(2)
            col1.image(os.path.join(image_folder, images[0]), use_column_width=True)
            if len(images) > 1:
                col2.image(os.path.join(image_folder, images[1]), use_column_width=True)

    time.sleep(1)
