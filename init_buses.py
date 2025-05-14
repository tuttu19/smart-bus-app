import sqlite3

conn = sqlite3.connect('data/smartbus.db')
cursor = conn.cursor()

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
print("✅ buses table created.")
