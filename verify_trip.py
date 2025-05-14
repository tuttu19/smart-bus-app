import streamlit as st
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from urllib.parse import urlencode

# === Email Config (update as needed) ===
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 587
SMTP_USER = "noreply@libragroupuae.com"
SMTP_PASS = "Libra@!183$!"  # ✅ Ensure this is correct

# === Determine trip type based on current hour ===
def get_trip_type():
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return "morning"
    elif 12 <= hour < 21:
        return "afternoon"
    else:
        return None

# === Fetch student info ===
def get_student(student_id):
    conn = sqlite3.connect("data/smartbus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, parent_email FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row if row else (None, None)

# === Log trip to trip_log table ===
def log_trip(student_id, trip_type):
    conn = sqlite3.connect("data/smartbus.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trip_log (student_id, trip_type) VALUES (?, ?)", (student_id, trip_type))
    conn.commit()
    conn.close()

# === Send confirmation email to parent ===
def send_confirmation_email(to_email, student_name, trip_type, confirm_link):
    subject = f"{student_name}'s {trip_type.capitalize()} Trip – Please Confirm"
    body = f"""
Dear Parent,

This is to notify you that {student_name} was scanned on the {trip_type} trip.

Please confirm the student’s safe arrival by clicking the link below:
{confirm_link}

Regards,
Smart Bus System
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

# === Streamlit UI ===
st.title("🚍 QR Scan Trip Verification")

# ✅ Read student ID from query string
sid = st.query_params.get("sid", [None])[0]

if not sid:
    st.warning("No student ID found in QR link.")
else:
    trip_type = get_trip_type()
    if not trip_type:
        st.error("❌ Scan is outside valid trip hours (5–9 AM or 12–9 PM).")
    else:
        student_name, parent_email = get_student(sid)
        if not student_name:
            st.error("❌ Invalid student ID.")
        else:
            log_trip(sid, trip_type)

            # 🔗 Confirmation URL for parent
            confirm_link = f"http://192.168.0.38.nip.io:8501/confirm_trip?{urlencode({'sid': sid, 'trip': trip_type})}"

            if parent_email:
                sent = send_confirmation_email(parent_email, student_name, trip_type, confirm_link)
                if sent:
                    st.success(f"✅ {trip_type.capitalize()} trip logged for {student_name}")
                    st.info("Parent has been emailed a confirmation link.")
                else:
                    st.warning("Trip logged, but failed to email parent.")
            else:
                st.warning("Trip logged, but no parent email found.")
