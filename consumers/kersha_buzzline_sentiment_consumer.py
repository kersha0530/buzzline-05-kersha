import sqlite3
import matplotlib.pyplot as plt
import time
import pandas as pd

# Database path
DB_PATH = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"

# Connect to SQLite and fetch sentiment data
def fetch_sentiment_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT category, COUNT(*) AS count
    FROM buzzline_messages
    WHERE timestamp >= datetime('now', '-10 minutes')
    GROUP BY category;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Plot function for real-time updates
def update_chart():
    plt.ion()
    fig, ax = plt.subplots()
    while True:
        df = fetch_sentiment_data()
        ax.clear()
        if not df.empty:
            ax.bar(df['category'], df['count'], color='skyblue')
            ax.set_xlabel("Category")
            ax.set_ylabel("Message Count")
            ax.set_title("Buzzline Sentiment Categories (Last 10 Minutes)")
            plt.xticks(rotation=45)
        else:
            ax.set_title("No Recent Data Available")
        plt.draw()
        plt.pause(2)  # Refresh every 2 seconds

if __name__ == "__main__":
    update_chart()
