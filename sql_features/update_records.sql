-- Standardizing category names
UPDATE buzzline_messages
SET category = 'tech'
WHERE category IN ('Technology', 'Tech');

UPDATE buzzline_messages
SET category = 'food'
WHERE category IN ('Foods', 'foodie', 'culinary');

-- Adjust sentiment scores if they are outside the expected range (-1 to 1)
UPDATE buzzline_messages
SET sentiment = 1.0
WHERE sentiment > 1;

UPDATE buzzline_messages
SET sentiment = -1.0
WHERE sentiment < -1;

-- Mark highly positive messages for review
UPDATE buzzline_messages
SET keyword_mentioned = 'Highly Positive'
WHERE sentiment > 0.9;
