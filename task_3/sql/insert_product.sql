INSERT INTO products (
    id, title, price, description, image, brand, model,
    color, category, popular, discount, on_sale
) VALUES (
    %(id)s, %(title)s, %(price)s, %(description)s, %(image)s, 
    %(brand)s, %(model)s, %(color)s, %(category)s, 
    %(popular)s, %(discount)s, %(on_sale)s
)
ON CONFLICT (id) DO UPDATE SET
    title = EXCLUDED.title,
    price = EXCLUDED.price,
    description = EXCLUDED.description,
    image = EXCLUDED.image,
    brand = EXCLUDED.brand,
    model = EXCLUDED.model,
    color = EXCLUDED.color,
    category = EXCLUDED.category,
    popular = EXCLUDED.popular,
    discount = EXCLUDED.discount,
    on_sale = EXCLUDED.on_sale