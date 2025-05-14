import streamlit as st
import sqlite3
import os
from PIL import Image
from datetime import datetime

# DB connection
def insert_student(name, grade, area, parent_email, photo_path):
    conn = sqlite3.connect('data/smartbus.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (name, grade, area, parent_email, profile_photo)
        VALUES (?, ?, ?, ?, ?)
    """, (name, grade, area, parent_email, photo_path))
    conn.commit()
    conn.close()

# UI
st.title("🧒 Register New Student")

with st.form("student_form", clear_on_submit=True):
    name = st.text_input("Full Name", max_chars=100)
    grade = st.text_input("Grade")
    area = st.text_input("Area")
    parent_email = st.text_input("Parent Email")
    profile_photo = st.file_uploader("Upload Profile Photo", type=["jpg", "png", "jpeg"])
    
    submitted = st.form_submit_button("Register Student")

    if submitted:
        if name and grade and area and parent_email:
            photo_path = ""
            if profile_photo:
                # Save photo
                ext = profile_photo.name.split('.')[-1]
                file_name = f"student_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                upload_dir = "static/uploads"
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                photo_path = os.path.join(upload_dir, file_name)
                with open(photo_path, "wb") as f:
                    f.write(profile_photo.getbuffer())
            
            insert_student(name, grade, area, parent_email, photo_path)
            st.success(f"✅ Student '{name}' registered successfully.")
        else:
            st.error("❗ All fields are required.")
