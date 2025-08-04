-- Insert top 10 most expensive products
TRUNCATE TABLE most_expensive;

INSERT INTO most_expensive (title, price, category)
SELECT 
    title,
    price,
    category
FROM products
ORDER BY price DESC
LIMIT 10;