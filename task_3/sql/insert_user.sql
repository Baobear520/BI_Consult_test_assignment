INSERT INTO users (
    id, name, address
) VALUES (
    %(id)s, %(name)s, %(address)s
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    address = EXCLUDED.address