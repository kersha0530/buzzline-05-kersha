SELECT category, COUNT(*) AS message_count, AVG(sentiment) AS avg_sentiment
FROM buzzline_messages
GROUP BY category
ORDER BY message_count DESC;
