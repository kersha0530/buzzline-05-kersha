import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import pathlib
from collections import defaultdict

# Define file path for sentiment storage
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT.joinpath("data", "buzzline_messages.json")

# Initialize sentiment categories
sentiment_counts = defaultdict(int)

# Initialize Matplotlib figure
fig, ax = plt.subplots()
plt.xticks(rotation=45)

# Function to categorize sentiment
def categorize_sentiment(score):
    if score < -0.3:
        return "Negative"
    elif score > 0.3:
        return "Positive"
    else:
        return "Neutral"

def read_sentiment_data():
    """Read sentiment values from `buzzline_messages.json`."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                return []  # No data available
            return [json.loads(line.strip()) for line in lines]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def update_chart(frame):
    """Fetch sentiment data, update bar chart."""
    global sentiment_counts

    # Reset counts
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}

    # Read and process messages
    messages = read_sentiment_data()
    for msg in messages:
        sentiment = categorize_sentiment(msg.get("sentiment", 0))
        sentiment_counts[sentiment] += 1

    # Clear previous chart and plot new data
    ax.clear()
    ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=["green", "yellow", "red"])
    ax.set_title("🚀 Buzzline Sentiment Distribution")
    ax.set_xlabel("Sentiment Category")
    ax.set_ylabel("Message Count")
    plt.tight_layout()

# Animation loop (updates every 2 seconds)
ani = animation.FuncAnimation(fig, update_chart, interval=2000)

# Run visualization
plt.show()
