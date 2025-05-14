import streamlit as st
import sqlite3

DB = "data/smartbus.db"

def get_unassigned_students():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, area FROM students WHERE bus_id IS NULL OR bus_id = ''")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_buses():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, areas_covered FROM buses")
    buses = cursor.fetchall()
    conn.close()
    return buses

def update_student_bus(student_id, bus_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET bus_id = ? WHERE id = ?", (bus_id, student_id))
    conn.commit()
    conn.close()

st.title("🚍 Auto Allocate Buses by Area")

unassigned = get_unassigned_students()
buses = get_all_buses()
allocated = 0

if st.button("Run Auto Allocation"):
    for sid, name, area in unassigned:
        for bus_id, areas in buses:
            if area.lower() in areas.lower():
                update_student_bus(sid, bus_id)
                allocated += 1
                break
    st.success(f"✅ {allocated} student(s) auto-allocated based on area.")

# Preview unassigned
st.subheader("🧒 Unassigned Students")
if unassigned:
    for sid, name, area in unassigned:
        st.write(f"🔸 {name} — Area: {area}")
else:
    st.info("✅ All students already have a bus assigned.")
