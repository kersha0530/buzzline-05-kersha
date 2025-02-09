-- 03_insert_records.sql
-- Inserts sample data into the users and buzzline_messages tables.
INSERT INTO users (name, email) VALUES
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Charlie Brown', 'charlie@example.com'),
    ('Eve Adams', 'eve@example.com'),
    ('Kersha Broussard', 'kersha@example.com');

INSERT INTO buzzline_messages (message, author_id, timestamp, category, sentiment, keyword_mentioned, message_length) VALUES
    ('I love Python!', 1, '2025-02-08 23:36:18', 'tech', 1.0, 'Python', 15),
    ('This new recipe is amazing!', 2, '2025-02-08 23:36:18', 'food', 0.8, 'recipe', 28),
    ('JavaScript is hard but useful.', 3, '2025-02-08 23:36:18', 'tech', 0.4, 'JavaScript', 31),
    ('I just watched a great movie.', 4, '2025-02-08 23:36:18', 'entertainment', 0.7, 'movie', 30),
    ('That meme was hilarious!', 5, '2025-02-08 23:36:18', 'humor', 0.9, 'meme', 23);
