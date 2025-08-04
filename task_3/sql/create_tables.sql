-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    brand VARCHAR(100),
    model VARCHAR(100),
    color VARCHAR(50),
    category VARCHAR(100),
    popular BOOLEAN DEFAULT FALSE,
    discount INTEGER,
    on_sale BOOLEAN DEFAULT FALSE
);

-- Create users table with JSON fields for name and address
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    name JSONB NOT NULL,
    address JSONB NOT NULL,
    phone VARCHAR(50)
);

-- Create most_expensive table for transformed data
CREATE TABLE IF NOT EXISTS most_expensive (
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100)
);

-- Create ods_users table for transformed user data
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