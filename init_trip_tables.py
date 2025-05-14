import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("data/smartbus.db")
cursor = conn.cursor()

# === Create trip_log table ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS trip_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    trip_type TEXT NOT NULL,
    log_time TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'completed'
)
""")

# === Create parent_confirm table ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS parent_confirm (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    trip_type TEXT NOT NULL,
    confirmed_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Tables trip_log and parent_confirm created (or already exist).")
