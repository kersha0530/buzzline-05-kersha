SELECT users.name, buzzline_messages.message, buzzline_messages.sentiment
FROM users
INNER JOIN buzzline_messages ON users.id = buzzline_messages.author_id
ORDER BY sentiment DESC;
