import sqlite3  # Ensure this is imported!
import os

# Define database path
db_path = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Run the update records SQL script
update_script_path = os.path.join("sql_features", "update_records.sql")
with open(update_script_path, "r") as f:
    cursor.executescript(f.read())

# Run the delete records SQL script
delete_script_path = os.path.join("sql_features", "delete_records.sql")
with open(delete_script_path, "r") as f:
    cursor.executescript(f.read())

# Commit changes and close connection
conn.commit()
conn.close()

print("Database feature updates applied successfully!")
