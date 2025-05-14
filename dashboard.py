import streamlit as st
import sqlite3
from datetime import datetime
import requests

# === Database Connection ===
conn = sqlite3.connect("data/smartbus.db")
cursor = conn.cursor()

# === Fetch Counts ===
total_students = cursor.execute("SELECT COUNT(*) FROM students").fetchone()[0]
assigned_students = cursor.execute("SELECT COUNT(*) FROM students WHERE bus_id IS NOT NULL").fetchone()[0]
unassigned_students = total_students - assigned_students
total_buses = cursor.execute("SELECT COUNT(*) FROM buses").fetchone()[0]
conn.close()

# === UI Instruction ===
st.markdown("### 🚌 Welcome, admin!")
st.info("ℹ️ Use the sidebar to manage buses, register students, assign them, and monitor trips.")

# === Metric Cards ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div style='border:2px solid #007bff; border-radius:8px; padding:15px;'>"
                "<h6>Total Students</h6><h3 style='color:#007bff'>" + str(total_students) + "</h3></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='border:2px solid #28a745; border-radius:8px; padding:15px;'>"
                "<h6>Assigned Students</h6><h3 style='color:#28a745'>" + str(assigned_students) + "</h3></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='border:2px solid #dc3545; border-radius:8px; padding:15px;'>"
                "<h6>Unassigned</h6><h3 style='color:#dc3545'>" + str(unassigned_students) + "</h3></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div style='border:2px solid #ffc107; border-radius:8px; padding:15px;'>"
                "<h6>Total Buses</h6><h3 style='color:#ffc107'>" + str(total_buses) + "</h3></div>", unsafe_allow_html=True)

# === Time & Weather (Optional) ===
col5, col6 = st.columns(2)

# Clock
with col5:
    now = datetime.now().strftime("%H:%M:%S")
    st.markdown("<div style='border:1px solid #ccc; border-radius:8px; padding:15px;'>"
                "<h6>⏰ Current Time (UAE)</h6><h3>" + now + "</h3></div>", unsafe_allow_html=True)

# Weather
with col6:
    try:
        res = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Dubai,AE&appid=dd22e6f3f1b3f049c755b01f1c6b4a74&units=metric").json()
        weather = res['weather'][0]['description']
        temp = res['main']['temp']
        st.markdown(f"<div style='border:1px solid #ccc; border-radius:8px; padding:15px;'>"
                    f"<h6>🌤 Dubai Weather</h6><h3>{temp}°C – {weather}</h3></div>", unsafe_allow_html=True)
    except:
        st.warning("Unable to fetch weather.")
