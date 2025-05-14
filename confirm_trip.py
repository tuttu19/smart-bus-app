import streamlit as st
import sqlite3
from datetime import datetime

# === Streamlit Setup ===
st.title("📩 Parent Confirmation")

# === Extract query parameters ===
sid = st.query_params.get("sid", [None])[0]
trip = st.query_params.get("trip", [None])[0]

if not sid or not trip:
    st.warning("Missing student ID or trip type in confirmation link.")
else:
    # === Confirm in DB ===
    conn = sqlite3.connect("data/smartbus.db")
    cursor = conn.cursor()

    # Check if already confirmed
    cursor.execute("""
        SELECT confirmed_at FROM parent_confirm
        WHERE student_id = ? AND trip_type = ? AND DATE(confirmed_at) = DATE('now')
    """, (sid, trip))
    existing = cursor.fetchone()

    if existing:
        st.success("✅ This trip was already confirmed.")
        st.caption(f"Confirmed at: {existing[0]}")
    else:
        cursor.execute("""
            INSERT INTO parent_confirm (student_id, trip_type, confirmed_at)
            VALUES (?, ?, ?)
        """, (sid, trip, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        st.success("✅ Thank you! You have successfully confirmed the student's safe arrival.")

    conn.close()
