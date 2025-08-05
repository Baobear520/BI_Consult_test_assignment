INSERT INTO users (
    id, name, address, created_at, updated_at
) VALUES (
    %(id)s, %(name)s, %(address)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    address = EXCLUDED.address,
    updated_at = CURRENT_TIMESTAMP