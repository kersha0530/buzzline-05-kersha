-- Remove duplicate messages based on message content & author
DELETE FROM buzzline_messages
WHERE id NOT IN (
    SELECT MIN(id) FROM buzzline_messages GROUP BY message, author
);

-- Remove messages containing spam keywords
DELETE FROM buzzline_messages
WHERE LOWER(message) LIKE '%free money%'
   OR LOWER(message) LIKE '%click here%'
   OR LOWER(message) LIKE '%win a prize%';

-- Remove extreme negative sentiment messages marked as inappropriate
DELETE FROM buzzline_messages
WHERE sentiment = -1.0
AND keyword_mentioned = 'inappropriate';
