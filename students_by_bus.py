import streamlit as st
import sqlite3

st.markdown("### 🧒 Students Grouped by Bus")

# Connect to database
conn = sqlite3.connect("data/smartbus.db")
cursor = conn.cursor()

# Fetch all buses
buses = cursor.execute("SELECT id, bus_name FROM buses ORDER BY bus_name").fetchall()

if not buses:
    st.warning("No buses found.")
else:
    for bus_id, bus_name in buses:
        # Fetch students for this bus
        students = cursor.execute("""
            SELECT name, grade, area
            FROM students
            WHERE bus_id = ?
            ORDER BY name
        """, (bus_id,)).fetchall()

        with st.expander(f"🚌 {bus_name} ({len(students)} students)"):
            if not students:
                st.info("No students assigned to this bus yet.")
            else:
                st.table([
                    {"Name": s[0], "Grade": s[1], "Area": s[2]}
                    for s in students
                ])

conn.close()
