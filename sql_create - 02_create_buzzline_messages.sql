-- Drop table if it exists to prevent duplicates
DROP TABLE IF EXISTS buzzline_messages;

-- Create new table with necessary fields
CREATE TABLE buzzline_messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    sentiment REAL NOT NULL,
    sentiment_label TEXT NOT NULL,
    keyword_mentioned TEXT,
    message_length INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    hour_of_day INTEGER NOT NULL
);
