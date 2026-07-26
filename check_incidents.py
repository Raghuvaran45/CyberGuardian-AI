import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/incidents.db"
)

df = pd.read_sql(
    "SELECT * FROM incidents ORDER BY id DESC LIMIT 5",
    conn
)

print(df)

conn.close()