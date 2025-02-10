import json
import os
import pathlib
import random
import sys
import time
from datetime import datetime
from utils.utils_logger import logger

# ✅ Path to the JSON file where the producer writes data
LIVE_DATA_FILE = pathlib.Path("C:/44608 projects spring 2025/buzzline-05-kersha/data/project_live.json")

# ✅ Define message generator
def generate_messages():
    ADJECTIVES = ["amazing", "funny", "boring", "exciting", "weird"]
    ACTIONS = ["found", "saw", "tried", "shared", "loved"]
    TOPICS = ["a movie", "a meme", "an app", "Python", "JavaScript", "recipe", "travel", "game"]
    AUTHORS = ["Alice", "Bob", "Charlie", "Eve", "Kersha"]

    CATEGORY_MAP = {
        "meme": "humor",
        "Python": "tech",
        "JavaScript": "tech",
        "recipe": "food",
        "travel": "travel",
        "movie": "entertainment",
        "game": "gaming",
    }

    while True:
        adjective = random.choice(ADJECTIVES)
        action = random.choice(ACTIONS)
        topic = random.choice(TOPICS)
        author = random.choice(AUTHORS)
        message_text = f"I just {action} {topic}! It was {adjective}."
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Find category
        keyword_mentioned = next((word for word in CATEGORY_MAP if word in topic), "other")
        category = CATEGORY_MAP.get(keyword_mentioned, "other")

        # Sentiment (randomized)
        sentiment = round(random.uniform(-1, 1), 2)

        # Create JSON message
        json_message = {
            "message": message_text,
            "author": author,
            "timestamp": timestamp,
            "category": category,
            "sentiment": sentiment,
            "keyword_mentioned": keyword_mentioned,
            "message_length": len(message_text),
        }

        yield json_message

# ✅ Main function (writes only to JSON, ignores Kafka)
def main():
    logger.info("🚀 Running JSON-based Producer...")

    # Ensure folder exists
    os.makedirs(LIVE_DATA_FILE.parent, exist_ok=True)

    try:
        while True:
            message = next(generate_messages())

            # Append to JSON file
            with LIVE_DATA_FILE.open("a") as f:
                f.write(json.dumps(message) + "\n")

            logger.info(f"📌 Generated: {message}")
            time.sleep(2)  # Adjust interval as needed

    except KeyboardInterrupt:
        logger.warning("⚠️ Producer stopped by user.")

if __name__ == "__main__":
    main()
