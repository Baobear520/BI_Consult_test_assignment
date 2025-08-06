-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    brand VARCHAR(63),
    model VARCHAR(255),
    color VARCHAR(63),
    category VARCHAR(63),
    popular BOOLEAN DEFAULT FALSE,
    discount INTEGER,
    on_sale BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table with JSON fields for name and address
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name JSONB NOT NULL,
    address JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create most_expensive table for transformed data
CREATE TABLE IF NOT EXISTS most_expensive (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(63),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ods_users table for transformed user data
CREATE TABLE IF NOT EXISTS ods_users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(63),
    lastname VARCHAR(63),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    street_number VARCHAR(31),
    street_name VARCHAR(63),
    zipcode VARCHAR(31),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products index for price sorting
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price DESC);

