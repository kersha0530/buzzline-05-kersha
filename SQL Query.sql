SELECT category, AVG(sentiment) AS avg_sentiment
FROM messages
GROUP BY category
ORDER BY avg_sentiment DESC;
