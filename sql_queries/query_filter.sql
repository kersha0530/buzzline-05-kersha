SELECT * FROM buzzline_messages
WHERE sentiment > 0.8 OR sentiment < -0.8
ORDER BY sentiment DESC;
