import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Database path
DB_PATH = "C:/44608 projects spring 2025/buzzline-05-kersha/buzzline05_kersha.sqlite"

# Function to fetch sentiment trend data
def fetch_sentiment_trends():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT category, COUNT(*) AS count
    FROM buzzline_messages
    WHERE timestamp >= datetime('now', '-60 minutes')
    GROUP BY category;


    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to fetch category counts
def fetch_category_counts():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT category, COUNT(*) AS count
    FROM buzzline_messages
    WHERE timestamp >= datetime('now', '-60 minutes')
    GROUP BY category;



    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Initialize Matplotlib figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Update both charts dynamically
def update_charts(frame):
    # Line chart - Sentiment trend
    ax1.clear()
    sentiment_data = fetch_sentiment_trends()
    if not sentiment_data.empty:
        ax1.plot(sentiment_data['timestamp'], sentiment_data['sentiment'], marker="o", linestyle="-", color="blue")
        ax1.set_title("Sentiment Trend Over Time")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Sentiment Score")
        ax1.axhline(0, color="gray", linestyle="dashed", linewidth=1)  # Neutral reference line
        ax1.tick_params(axis="x", rotation=45)
    else:
        ax1.set_title("No Sentiment Data Available")

    # Bar chart - Category counts
    ax2.clear()
    category_data = fetch_category_counts()
    if not category_data.empty:
        ax2.bar(category_data['category'], category_data['count'], color="skyblue")
        ax2.set_title("Message Count per Category (Last 10 Minutes)")
        ax2.set_xlabel("Category")
        ax2.set_ylabel("Message Count")
        ax2.tick_params(axis="x", rotation=45)
    else:
        ax2.set_title("No Category Data Available")

    plt.tight_layout()

# Run animation to update charts every 2 seconds
ani = animation.FuncAnimation(fig, update_charts, interval=2000)

# Show visualization
plt.show()
