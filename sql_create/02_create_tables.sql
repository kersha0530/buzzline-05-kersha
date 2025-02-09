-- 02_create_tables.sql
-- Creates the necessary tables with foreign key relationships.
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE buzzline_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    author_id INTEGER,
    timestamp TEXT NOT NULL,
    category TEXT NOT NULL,
    sentiment REAL,
    keyword_mentioned TEXT,
    message_length INTEGER,
    FOREIGN KEY (author_id) REFERENCES users (id)
);