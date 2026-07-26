import sqlite3

conn = sqlite3.connect("database/incidents.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(incidents)")
print(cursor.fetchall())

conn.close()