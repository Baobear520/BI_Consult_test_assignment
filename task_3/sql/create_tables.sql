-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    image VARCHAR(255)
);

-- Create users table with JSON fields
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name JSONB NOT NULL,
    address JSONB NOT NULL
);

-- Create most_expensive table
CREATE TABLE IF NOT EXISTS most_expensive (
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100)
);

-- Create ods_users table
CREATE TABLE IF NOT EXISTS ods_users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    street_number VARCHAR(20),
    street_name VARCHAR(255),
    zipcode VARCHAR(20)
);