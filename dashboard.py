# dashboard.py (on Device 2)
import pandas as pd
import streamlit as st
import socket
import threading
import cv2
import os
import time
from datetime import datetime

st.set_page_config(page_title="🛰️ Aerospace Telemetry", layout="wide")

csv_file = "telemetry_log.csv"
image_folder = "captured_images"
os.makedirs(image_folder, exist_ok=True)

# Live DataFrame (avoid reading file repeatedly)
if "df" not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(csv_file)
    except:
        st.session_state.df = pd.DataFrame(columns=["UTC Timestamp", "Altitude", "Speed", "Temperature"])
        st.session_state.df.to_csv(csv_file, index=False)

# Telemetry Receiver Thread
def receive_data():
    HOST = '0.0.0.0'  # Accept connections from any IP
    PORT = 5000
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[✓] Listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    print(f"[+] Connected by {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if data:
                a, sp, tp = map(int, data.split(','))
                utc_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                new_row = {
                    "UTC Timestamp": utc_now,
                    "Altitude": a,
                    "Speed": sp,
                    "Temperature": tp
                }

                st.session_state.df.loc[len(st.session_state.df)] = new_row
                st.session_state.df.to_csv(csv_file, index=False)
        except:
            break

# Webcam Capture Thread
def capture_images_periodically():
    cap = cv2.VideoCapture(0)
    while True:
        time.sleep(20)
        for i in range(2):
            ret, frame = cap.read()
            if ret:
                filename = f"{image_folder}/capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.jpg"
                cv2.imwrite(filename, frame)
    cap.release()

# Start threads once
if "threads_started" not in st.session_state:
    threading.Thread(target=receive_data, daemon=True).start()
    threading.Thread(target=capture_images_periodically, daemon=True).start()
    st.session_state.threads_started = True

# UI
st.title("🛰️ Aerospace Telemetry Dashboard")
st.markdown("Minimalist real-time dashboard for aircraft telemetry.")

df = st.session_state.df

if not df.empty:
    latest = df.iloc[-1]
    st.markdown("### 🔍 Real-time Readings")
    col1, col2, col3 = st.columns(3)
    col1.metric("📡 Altitude (ft)", f"{latest['Altitude']}")
    col2.metric("🚀 Speed (km/h)", f"{latest['Speed']}")
    col3.metric("🌡️ Temperature (°C)", f"{latest['Temperature']}")

    st.markdown("### 📈 Graphs (Last 30 Readings)")
    chart_df = df.tail(30).copy()
    chart_df["UTC Timestamp"] = pd.to_datetime(chart_df["UTC Timestamp"])
    chart_df.set_index("UTC Timestamp", inplace=True)

    st.subheader("📡 Altitude")
    st.line_chart(chart_df["Altitude"])

    st.subheader("🚀 Speed")
    st.line_chart(chart_df["Speed"])

    st.subheader("🌡️ Temperature")
    st.line_chart(chart_df["Temperature"])

    st.markdown("### 📷 Latest Captured Images")
    image_files = sorted(os.listdir(image_folder), reverse=True)[:2]
    if image_files:
        col1, col2 = st.columns(2)
        for idx, file in enumerate(image_files):
            img_path = os.path.join(image_folder, file)
            if idx == 0:
                col1.image(img_path, caption="Capture 1", use_column_width=True)
            else:
                col2.image(img_path, caption="Capture 2", use_column_width=True)
else:
    st.info("Waiting for telemetry data...")
