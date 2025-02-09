# db01_setup.py
# Sets up the SQLite database and creates tables.
import sqlite3

db_path = "buzzline05_kersha.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open("sql_create/01_drop_tables.sql", "r") as f:
    cursor.executescript(f.read())

with open("sql_create/02_create_tables.sql", "r") as f:
    cursor.executescript(f.read())

with open("sql_create/03_insert_records.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()
print("Database setup complete!")