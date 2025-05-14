import streamlit as st
import sqlite3
import os
from PIL import Image

# DB fetch
def get_students():
    conn = sqlite3.connect('data/smartbus.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, grade, area, parent_email, profile_photo FROM students ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Page config
st.title("📋 Registered Students")

students = get_students()

# Search
search_term = st.text_input("🔍 Search by name, grade or area").lower()

# Display
for s in students:
    name, grade, area, parent_email, photo_path = s
    combined = f"{name} {grade} {area}".lower()
    if search_term in combined or search_term == "":
        col1, col2 = st.columns([1, 4])
        with col1:
            if photo_path and os.path.exists(photo_path):
                st.image(photo_path, width=100)
            else:
                st.image("https://via.placeholder.com/100x100?text=No+Photo", width=100)
        with col2:
            st.markdown(f"**👤 Name:** {name}")
            st.markdown(f"**🎓 Grade:** {grade}")
            st.markdown(f"**📍 Area:** {area}")
            st.markdown(f"**📧 Parent Email:** {parent_email}")
        st.divider()
