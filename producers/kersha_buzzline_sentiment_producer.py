import sqlite3
import random
import time
from datetime import datetime

# Database path
DB_PATH = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"

# Define categories and messages
CATEGORIES = {
    "tech": ["Python is amazing!", "AI is revolutionizing everything!"],
    "food": ["This recipe is delicious!", "Best pasta ever!"],
    "humor": ["That meme cracked me up!", "Hilarious joke of the day!"],
    "travel": ["Just visited an incredible place!", "Traveling is life-changing!"],
}
AUTHORS = ["Alice", "Bob", "Charlie", "Eve", "Kersha"]

# Ensure table exists
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buzzline_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        author TEXT,
        timestamp TEXT,
        category TEXT,
        sentiment REAL
    );
    """)
    conn.commit()
    conn.close()

# Generate messages
def generate_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        category = random.choice(list(CATEGORIES.keys()))
        message = random.choice(CATEGORIES[category])
        author = random.choice(AUTHORS)
        sentiment = round(random.uniform(-1, 1), 2)
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
        INSERT INTO buzzline_messages (message, author, timestamp, category, sentiment)
        VALUES (?, ?, ?, ?, ?);
        """, (message, author, timestamp, category, sentiment))
        
        conn.commit()
        print(f"Inserted: {message} | Category: {category} | Sentiment: {sentiment}")
        time.sleep(2)  # Adjust interval as needed

if __name__ == "__main__":
    setup_database()
    generate_messages()
