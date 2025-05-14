import streamlit as st
import sqlite3
import os
from datetime import datetime

UPLOAD_DIR = "static/uploads"
DB_PATH = "data/smartbus.db"

# Ensure upload folder exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Save to database
def insert_bus(bus_name, capacity, city, areas_covered, driver_name, driver_contact, photo_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO buses (bus_name, capacity, city, areas_covered, driver_name, driver_contact, driver_photo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (bus_name, capacity, city, areas_covered, driver_name, driver_contact, photo_path))
    conn.commit()
    conn.close()

# UI
st.title("🚌 Add Bus and Driver")

with st.form("bus_form", clear_on_submit=True):
    bus_name = st.text_input("Bus Name")
    capacity = st.number_input("Capacity", min_value=1, max_value=100, step=1)
    city = st.selectbox("City (Emirate)", ["", "Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Umm Al Quwain", "Ras Al Khaimah", "Fujairah"])
    areas_covered = st.text_area("Areas Covered", help="e.g. Al Nahda, Muhaisnah 3, Lulu Village")
    
    driver_name = st.text_input("Driver Name")
    driver_contact = st.text_input("Driver Contact No")
    driver_photo = st.file_uploader("Upload Driver Photo", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("➕ Add Bus")

    if submitted:
        if bus_name and capacity and city and areas_covered and driver_name and driver_contact:
            photo_path = ""
            if driver_photo:
                ext = driver_photo.name.split(".")[-1]
                file_name = f"driver_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                photo_path = os.path.join(UPLOAD_DIR, file_name)
                with open(photo_path, "wb") as f:
                    f.write(driver_photo.getbuffer())

            insert_bus(bus_name, capacity, city, areas_covered, driver_name, driver_contact, photo_path)
            st.success("✅ Bus and driver added successfully.")
        else:
            st.error("❗ All fields are required.")
