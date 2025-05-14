import streamlit as st
from pathlib import Path

# === Page Config ===
st.set_page_config(page_title="Smart Bus Management System", layout="wide")

# === Sticky Header & Padding Fix ===
st.markdown("""
    <style>
        /* Sticky Top Header */
        .custom-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100%;
            background-color: #0e1117;
            padding: 1rem 2rem;
            color: white;
            font-size: 26px;
            font-weight: bold;
            z-index: 9999;
            border-bottom: 1px solid #444;
        }

        .custom-header h1 {
            margin: 0;
        }

        /* Push content below the fixed header */
        .block-container {
            padding-top: 100px !important;
        }

        /* Responsive: Adjust padding when sidebar collapses */
        @media (max-width: 768px) {
            .custom-header {
                padding-left: 2.5rem;
                font-size: 22px;
            }
        }
    </style>

    <div class="custom-header">
        <h1>🚌 Smart Bus Management System</h1>
    </div>
""", unsafe_allow_html=True)

# === Sidebar Navigation ===
st.sidebar.title("📂 Navigation")
menu_options = [
    "📊 Dashboard",
    "🧒 Register Student",
    "📋 View Students",
    "🚌 Add Bus",
    "🧾 View Buses",
    "🧒 Students Grouped by Bus",
    "⚙️ Auto Allocate",
    "📎 Generate Assignment Slip",
    "🗂 Trip Logs",
    "🔍 Verify Trip (QR Scan)",
    "✅ Confirm Trip (Parent)"
]
selected_menu = st.sidebar.radio("Go to", menu_options, index=0)

# === Page Modules Map ===
module_files = {
    "📊 Dashboard": "dashboard.py",
    "🧒 Register Student": "register_student.py",
    "📋 View Students": "view_students.py",
    "🧒 Students Grouped by Bus": "students_by_bus.py",
    "🚌 Add Bus": "add_bus.py",
    "🧾 View Buses": "view_buses.py",
    "⚙️ Auto Allocate": "auto_allocate.py",
    "📎 Generate Assignment Slip": "student_slip_generator.py",
    "🗂 Trip Logs": "trip_logs.py",
    "🔍 Verify Trip (QR Scan)": "verify_trip.py",
    "✅ Confirm Trip (Parent)": "confirm_trip.py"
}

# === Execute Selected Module ===
file_path = module_files.get(selected_menu)
if file_path and Path(file_path).exists():
    try:
        exec(Path(file_path).read_text(encoding="utf-8"), globals())
    except Exception as e:
        st.error(f"❌ Error loading `{file_path}`:\n\n{e}")
else:
    st.warning("⚠️ Selected module not found.")
