import sqlite3
import json
from datetime import datetime

#  Function to categorize sentiment
def categorize_sentiment(score):
    if score < -0.3:
        return "Negative"
    elif score > 0.3:
        return "Positive"
    else:
        return "Neutral"

#  Adjust database and JSON file paths
db_path = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"
json_file_path = "C:/44608 projects spring 2025/buzzline-05-kersha/data/buzzline_data.json"


#  Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#  Ensure the table exists before inserting
create_table_query = """
CREATE TABLE IF NOT EXISTS buzzline_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    author TEXT,
    timestamp TEXT,
    category TEXT,
    sentiment REAL,
    sentiment_label TEXT,
    keyword_mentioned TEXT,
    message_length INTEGER,
    hour_of_day INTEGER
);
"""
cursor.execute(create_table_query)
conn.commit()

#  Load JSON data and insert into SQLite
try:
    with open(json_file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())

            # Extract message details
            message_text = data.get("message", "").strip()
            author = data.get("author", "Unknown")
            category = data.get("category", "other")
            sentiment = data.get("sentiment", 0.0)
            keyword_mentioned = data.get("keyword_mentioned", None)
            message_length = len(message_text)
            timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Convert timestamp to datetime and extract hour
            dt_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            hour_of_day = dt_obj.hour

            # Determine sentiment label
            sentiment_label = categorize_sentiment(sentiment)

            # Insert into SQLite database
            cursor.execute(
                """
                INSERT INTO buzzline_messages 
                (message, author, timestamp, category, sentiment, sentiment_label, keyword_mentioned, message_length, hour_of_day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (message_text, author, timestamp, category, sentiment, sentiment_label, keyword_mentioned, message_length, hour_of_day),
            )

    #  Commit changes
    conn.commit()
    print(" Data inserted into buzzline_messages successfully!")

except Exception as e:
    print(f"❌ Error inserting data: {e}")

finally:
    #  Close connection
    conn.close()
