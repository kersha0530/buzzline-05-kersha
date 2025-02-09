import sqlite3
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime

# Database path
DB_PATH = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"

# Time window for filtering messages (default: last 10 minutes)
TIME_WINDOW = "-10 minutes"

# Function to ensure the sentiment trends table exists
def ensure_sentiment_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS buzzline_sentiment_trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        timestamp TEXT,
        avg_sentiment REAL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Function to fetch average sentiment per category in the last X minutes
def fetch_sentiment_data():
    conn = sqlite3.connect(DB_PATH)
    query = f"""
    SELECT category, COUNT(*) AS count, AVG(sentiment) AS avg_sentiment
    FROM buzzline_messages
    WHERE timestamp >= datetime('now', '{TIME_WINDOW}')
    GROUP BY category;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to store sentiment trends in a separate table for historical analysis
def store_sentiment_trends():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    df = fetch_sentiment_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO buzzline_sentiment_trends (category, timestamp, avg_sentiment)
            VALUES (?, ?, ?)
            """,
            (row["category"], timestamp, row["avg_sentiment"])
        )

    conn.commit()
    conn.close()

# Function to fetch stored sentiment trends for visualization
def fetch_sentiment_trends():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT category, timestamp, avg_sentiment FROM buzzline_sentiment_trends
    ORDER BY timestamp ASC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to visualize sentiment trends over time
def update_charts():
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    while True:
        df = fetch_sentiment_data()
        df_trends = fetch_sentiment_trends()

        # Bar Chart: Current Sentiment per Category
        ax1.clear()
        if not df.empty:
            categories = df["category"]
            sentiment_values = df["avg_sentiment"]
            message_counts = df["count"]

            colors = ['red' if s < 0 else 'green' for s in sentiment_values]
            bars = ax1.bar(categories, sentiment_values, color=colors)

            # Display message counts above bars
            for bar, count in zip(bars, message_counts):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(count),
                         ha='center', va='bottom', fontsize=10)

            ax1.set_xlabel("Category")
            ax1.set_ylabel("Avg Sentiment Score")
            ax1.set_title(f"Sentiment Trends Per Category ({TIME_WINDOW} window)")
            ax1.set_ylim(-1, 1)
            plt.xticks(rotation=45)
        else:
            ax1.set_title("No Recent Data Available")

        # Line Chart: Sentiment Trends Over Time
        ax2.clear()
        if not df_trends.empty:
            for category in df_trends["category"].unique():
                subset = df_trends[df_trends["category"] == category]
                ax2.plot(subset["timestamp"], subset["avg_sentiment"], label=category, marker="o")

            ax2.set_xlabel("Time")
            ax2.set_ylabel("Avg Sentiment Score")
            ax2.set_title("Sentiment Trends Over Time")
            ax2.legend(loc="best")
            plt.xticks(rotation=45)
        else:
            ax2.set_title("No Historical Sentiment Data")

        plt.draw()
        plt.pause(5)  # Refresh every 5 seconds

        # Store new sentiment data into history table
        store_sentiment_trends()

# Ensure database table exists
ensure_sentiment_table()

if __name__ == "__main__":
    update_charts()

