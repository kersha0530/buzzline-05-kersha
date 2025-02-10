import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import time
import pathlib
import pandas as pd
from collections import deque
from datetime import datetime

# Define file path for sentiment storage
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT.joinpath("data", "sentiment_live.json")

# Store recent sentiment values
sentiment_values = deque(maxlen=50)  # Keep last 50 messages for trends
timestamps = deque(maxlen=50)

# Initialize Matplotlib figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle("Kersha's Buzzline Sentiment Analysis", fontsize=14)

# **Function to Read Sentiment Data from JSON**
def read_sentiment_data():
    """Read sentiment values from `sentiment_live.json` and return all messages."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, list) and len(data) > 0:
                return data  #  Return all messages, not just one
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    return []


#  **Function to Update the Charts**
def update_charts(frame):
    """Fetch all sentiment values from file, update both bar and line charts dynamically."""
    all_data = read_sentiment_data()

    if not all_data:
        ax1.clear()
        ax2.clear()
        ax1.set_title("No Sentiment Data Available")
        ax2.set_title("No Sentiment Trends Over Time")
        return

    # Extract timestamps and sentiment values
    timestamps.clear()
    sentiment_values.clear()
    categories = {}
    
    for entry in all_data[-50:]:  # ✅ Process last 50 messages
        timestamps.append(entry["timestamp"][-8:])  # Extract only HH:MM:SS
        sentiment_values.append(entry["sentiment"])
        
        category = entry.get("category", "other")
        categories[category] = categories.get(category, []) + [entry["sentiment"]]

    # **Update Bar Chart (Sentiment Per Category)**
    ax1.clear()
    avg_sentiments = {cat: sum(vals) / len(vals) for cat, vals in categories.items()}
    ax1.bar(avg_sentiments.keys(), avg_sentiments.values(), color=["green" if x > 0 else "red" for x in avg_sentiments.values()])
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


# **Animation loop (updates every 2 seconds)**
ani = animation.FuncAnimation(fig, update_charts, interval=2000, cache_frame_data=False)


# **Run visualization**
plt.show()







