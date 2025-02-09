import sqlite3
import random
import time
from datetime import datetime

# Database path
DB_PATH = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"

# Define categories, messages, and keyword sentiment mapping
CATEGORIES = {
    "tech": ["Python is amazing!", "AI is revolutionizing everything!"],
    "food": ["This recipe is delicious!", "Best pasta ever!"],
    "humor": ["That meme cracked me up!", "Hilarious joke of the day!"],
    "travel": ["Just visited an incredible place!", "Traveling is life-changing!"],
}
KEYWORD_SENTIMENT = {
    "amazing": 0.9,
    "delicious": 0.8,
    "hilarious": 0.7,
    "revolutionizing": 0.6,
    "best": 0.5,
    "cracked": 0.4,
    "life-changing": 0.3,
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
        sentiment REAL,
        keyword_mentioned TEXT,
        message_length INTEGER,
        hour_of_day INTEGER
    );
    """)
    conn.commit()
    conn.close()

# Generate sentiment based on keywords
def assess_sentiment(message):
    for word, score in KEYWORD_SENTIMENT.items():
        if word in message.lower():
            return round(score, 2)
    return round(random.uniform(-1, 1), 2)  # Fallback to random if no keyword matches

# Generate messages
def generate_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        category = random.choice(list(CATEGORIES.keys()))
        message = random.choice(CATEGORIES[category])
        author = random.choice(AUTHORS)
        sentiment = assess_sentiment(message)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        message_length = len(message)
        hour_of_day = datetime.utcnow().hour
        
        # Identify keyword mentioned
        keyword_mentioned = next((word for word in KEYWORD_SENTIMENT if word in message.lower()), None)

        cursor.execute("""
        INSERT INTO buzzline_messages (message, author, timestamp, category, sentiment, keyword_mentioned, message_length, hour_of_day)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (message, author, timestamp, category, sentiment, keyword_mentioned, message_length, hour_of_day))
        
        conn.commit()
        print(f"📝 Inserted: {message} | Category: {category} | Sentiment: {sentiment} | Keyword: {keyword_mentioned}")
        time.sleep(2)  # Adjust interval as needed

if __name__ == "__main__":
    setup_database()
    generate_messages()

