import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import pathlib
import pandas as pd
from collections import deque
from datetime import datetime

# Define file paths
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT.joinpath("data", "sentiment_live.json")
DB_PATH = PROJECT_ROOT.joinpath("buzzline05_kersha.sqlite")

# Store recent sentiment values
sentiment_values = deque(maxlen=50)  # Track last 50 sentiment values
timestamps = deque(maxlen=50)

# Initialize Matplotlib figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle("Kersha's Buzzline Sentiment Analysis", fontsize=14)

# 📌 **Ensure SQLite Table Exists**
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buzzline_processed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        author TEXT,
        timestamp TEXT,
        category TEXT,
        sentiment REAL,
        sentiment_label TEXT,
        keyword_mentioned TEXT,
        message_length INTEGER
    );
    """)
    
    conn.commit()
    conn.close()

# 📌 **Read Latest Message from JSON**
def read_latest_message():
    """Reads and returns the most recent message from `sentiment_live.json`."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, list) and len(data) > 0:
                return data[-1]  # Return only the latest message
    except (json.JSONDecodeError, FileNotFoundError):
        return None
    return None

# 📌 **Process & Store Message in SQLite**
def process_and_store_message(message):
    """Processes and saves each message individually into SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Extract message details
    sentiment = message.get("sentiment", 0)
    category = message.get("category", "other")
    timestamp = message.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    author = message.get("author", "Unknown")
    text = message.get("message", "")
    keyword_mentioned = message.get("keyword_mentioned", None)
    message_length = len(text)

    # Categorize sentiment
    if sentiment > 0.3:
        sentiment_label = "Positive"
    elif sentiment < -0.3:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    # Insert into database
    cursor.execute("""
        INSERT INTO buzzline_processed (message, author, timestamp, category, sentiment, sentiment_label, keyword_mentioned, message_length)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (text, author, timestamp, category, sentiment, sentiment_label, keyword_mentioned, message_length))

    conn.commit()
    conn.close()
    print(f"✅ Stored: {text} | Sentiment: {sentiment_label} | Category: {category}")

# 📌 **Update Visualization**
def update_charts(frame):
    """Fetches new sentiment values and updates bar & line charts dynamically."""
    new_data = read_latest_message()

    if new_data:
        process_and_store_message(new_data)  # Store new message in database

        timestamp = datetime.now().strftime("%H:%M:%S")
        sentiment = new_data.get("sentiment", 0)
        category = new_data.get("category", "other")

        # Store data for visualization
        timestamps.append(timestamp)
        sentiment_values.append(sentiment)

        # **Update Bar Chart (Sentiment Per Category)**
        ax1.clear()
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT category, AVG(sentiment) AS avg_sentiment FROM buzzline_processed GROUP BY category", conn)
        conn.close()

        if not df.empty:
            ax1.bar(df["category"], df["avg_sentiment"], color=["green" if s > 0 else "red" for s in df["avg_sentiment"]])
            ax1.set_title("📊 Sentiment Trends Per Category")
            ax1.set_xlabel("Category")
            ax1.set_ylabel("Avg Sentiment Score")
            ax1.set_ylim(-1, 1)

        # **Update Line Chart (Sentiment Over Time)**
        ax2.clear()
        ax2.plot(timestamps, sentiment_values, marker="o", linestyle="-", color="blue")
        ax2.axhline(0, color="gray", linestyle="dashed", linewidth=1)
        ax2.set_title("📈 Sentiment Trends Over Time")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Sentiment Score")
        plt.xticks(rotation=45)

        plt.tight_layout()

# 📌 **Setup Database Before Running**
setup_database()

# **Animation loop (updates every 2 seconds)**
ani = animation.FuncAnimation(fig, update_charts, interval=2000)

# **Run visualization**
plt.show()








