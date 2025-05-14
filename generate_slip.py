from fpdf import FPDF
import sqlite3
import os
from datetime import datetime
from generate_qr import generate_qr  # must return PNG path

PDF_DIR = "generated_pdfs"

def get_student_data(student_id):
    conn = sqlite3.connect("data/smartbus.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name, s.grade, s.area, s.parent_email, s.profile_photo,
               b.bus_name, b.driver_name, b.driver_contact, b.areas_covered
        FROM students s
        LEFT JOIN buses b ON s.bus_id = b.id
        WHERE s.id = ? AND s.bus_id IS NOT NULL
    """, (student_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def generate_pdf(student_id):
    data = get_student_data(student_id)
    if not data:
        return None

    name, grade, area, parent_email, profile_photo, bus_name, driver_name, driver_contact, areas_covered = data

    # Create QR code that encodes trip verification URL
    verify_url = f"http://192.168.0.38:8501/verify_trip?sid={student_id}"
    qr_path = generate_qr(verify_url, f"{student_id}_trip.png")

    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Student Bus Assignment Slip", ln=True, align="C")
    pdf.ln(10)

    # Student Info
    pdf.set_font("Arial", "", 12)
    pdf.cell(50, 10, "Student Name:", 0)
    pdf.cell(0, 10, name, ln=True)

    pdf.cell(50, 10, "Grade:", 0)
    pdf.cell(0, 10, grade, ln=True)

    pdf.cell(50, 10, "Area:", 0)
    pdf.cell(0, 10, area, ln=True)

    pdf.cell(50, 10, "Bus Name:", 0)
    pdf.cell(0, 10, bus_name, ln=True)

    pdf.cell(50, 10, "Driver Name:", 0)
    pdf.cell(0, 10, driver_name, ln=True)

    pdf.cell(50, 10, "Contact:", 0)
    pdf.cell(0, 10, driver_contact, ln=True)

    pdf.cell(50, 10, "Areas Covered:", 0)
    pdf.multi_cell(0, 10, areas_covered or "—")

    # QR Code
    pdf.ln(10)
    pdf.cell(0, 10, "Scan QR for Bus Attendance:", ln=True)
    pdf.image(qr_path, x=80, y=pdf.get_y(), w=40)


    # Footer
    pdf.ln(30)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Issued on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    # Save to directory
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)

    output_path = os.path.join(PDF_DIR, f"Bus_Assignment_{student_id}.pdf")
    pdf.output(output_path)
    return output_path