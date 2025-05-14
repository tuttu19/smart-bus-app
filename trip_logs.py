import streamlit as st
import sqlite3

conn = sqlite3.connect("data/smartbus.db")
cursor = conn.cursor()

logs = cursor.execute("""
    SELECT t.student_id, s.name, t.trip_type, t.log_time,
           pc.confirmed_at
    FROM trip_log t
    JOIN students s ON t.student_id = s.id
    LEFT JOIN parent_confirm pc
        ON pc.student_id = t.student_id
        AND pc.trip_type = t.trip_type
        AND DATE(pc.confirmed_at) = DATE(t.log_time)
    ORDER BY t.log_time DESC
""").fetchall()

conn.close()

st.markdown("### 🗂 Trip Attendance Logs")

if not logs:
    st.info("No trip logs found.")
else:
    st.table([
        {
            "Student": name,
            "Trip Type": trip_type.capitalize(),
            "Time": log_time,
            "Parent Confirmed": "✅ Yes" if confirmed_at else "❌ No"
        }
        for _, name, trip_type, log_time, confirmed_at in logs
    ])
