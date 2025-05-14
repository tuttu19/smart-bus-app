import streamlit as st
import sqlite3
import os
from generate_slip import generate_pdf

# Load student list
def get_students():
    conn = sqlite3.connect('data/smartbus.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM students ORDER BY name ASC")
    data = cursor.fetchall()
    conn.close()
    return data

st.title("📎 Generate Student Assignment Slip")

students = get_students()
student_names = {f"{name} (ID: {sid})": sid for sid, name in students}

if students:
    selected = st.selectbox("Select Student", list(student_names.keys()))
    selected_id = student_names[selected]

    if st.button("Generate PDF Slip"):
        output = generate_pdf(selected_id)
        if output and os.path.exists(output):
            with open(output, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name=os.path.basename(output))
                st.success("✅ Slip generated successfully.")
        else:
            st.error("❌ Failed to generate slip.")
else:
    st.info("No students registered yet.")
