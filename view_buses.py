import streamlit as st
import sqlite3
import os

conn = sqlite3.connect("data/smartbus.db")
cursor = conn.cursor()

buses = cursor.execute("SELECT * FROM buses ORDER BY bus_name ASC").fetchall()
conn.close()

st.markdown("### 🧾 Bus & Driver Summary")

# Search
search = st.text_input("🔍 Search by bus, driver, or city")

filtered_buses = [
    bus for bus in buses
    if search.lower() in " ".join(str(x).lower() for x in bus)
]

# Grid
for bus in filtered_buses:
    (
        bus_id, bus_name, capacity, city, areas, driver_name,
        driver_contact, driver_photo
    ) = bus

    col1, col2 = st.columns([1, 4])

    with col1:
        if driver_photo and os.path.exists(driver_photo):
            st.image(driver_photo, width=100)
        else:
            st.image("https://via.placeholder.com/100x100?text=No+Photo", width=100)

    with col2:
        st.markdown(f"#### {bus_name}")
        st.markdown(f"👤 **Driver:** {driver_name}")
        st.markdown(f"📞 **Contact:** {driver_contact}")
        st.markdown(f"🏙️ **City:** {city}")
        st.markdown(f"🧍 **Capacity:** {capacity}")
        st.markdown(f"📍 **Areas Covered:** {areas}")
        st.markdown("---")
