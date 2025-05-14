import sqlite3

conn = sqlite3.connect('data/smartbus.db')
cursor = conn.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    grade TEXT NOT NULL,
    area TEXT NOT NULL,
    parent_email TEXT NOT NULL,
    profile_photo TEXT,
    bus_id INTEGER
)
""")

# Create buses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_name TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    city TEXT NOT NULL,
    areas_covered TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    driver_contact TEXT NOT NULL,
    driver_photo TEXT
)
""")

conn.commit()
conn.close()
print("✅ New smartbus.db created with students and buses tables.")
