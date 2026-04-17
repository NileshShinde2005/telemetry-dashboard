import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Telemetry Dashboard", layout="wide")

st.title("🚀 Aerospace Telemetry System")

# placeholders
altitude_placeholder = st.empty()
speed_placeholder = st.empty()
temp_placeholder = st.empty()

graph_placeholder = st.empty()

# data storage
data = {
    "altitude": [],
    "speed": [],
    "temperature": []
}

# simulate real-time data
for i in range(1000):
    
    altitude = random.randint(100, 500)
    speed = random.randint(10, 300)
    temperature = random.randint(15, 50)

    data["altitude"].append(altitude)
    data["speed"].append(speed)
    data["temperature"].append(temperature)

    # display live values
    altitude_placeholder.metric("Altitude (m)", altitude)
    speed_placeholder.metric("Speed (km/h)", speed)
    temp_placeholder.metric("Temperature (°C)", temperature)

    # create dataframe
    df = pd.DataFrame(data)

    # plot graphs
    fig, ax = plt.subplots()
    ax.plot(df["altitude"], label="Altitude")
    ax.plot(df["speed"], label="Speed")
    ax.plot(df["temperature"], label="Temperature")
    ax.legend()

    graph_placeholder.pyplot(fig)

    time.sleep(1)
