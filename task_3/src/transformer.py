"""Data transformation module."""
import os
import logging
from typing import List, Dict, Any
from database import DatabaseConnection, execute_sql_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataTransformer:
    """Handle data transformations and database operations."""
    
    def __init__(self):
        """Initialize transformer with SQL scripts directory path."""
        self.sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql')

    def create_tables(self) -> None:
        """Create database tables."""
        sql_file = os.path.join(self.sql_dir, 'create_tables.sql')
        with DatabaseConnection() as cursor:
            execute_sql_file(cursor, sql_file)
            logger.info("Database tables created successfully")

    def load_products(self, products: List[Dict[str, Any]]) -> None:
        """Load products data into database."""
        with DatabaseConnection() as cursor:
            for product in products:
                cursor.execute(
                    """
                    INSERT INTO products (title, price, description, category, image)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        product['title'],
                        product['price'],
                        product['description'],
                        product['category'],
                        product['image']
                    )
                )
            logger.info(f"Loaded {len(products)} products into database")

    def load_users(self, users: List[Dict[str, Any]]) -> None:
        """Load users data into database."""
        with DatabaseConnection() as cursor:
            for user in users:
                cursor.execute(
                    """
                    INSERT INTO users (name, address)
                    VALUES (%s, %s)
                    """,
                    (
                        user['name'],
                        user['address']
                    )
                )
            logger.info(f"Loaded {len(users)} users into database")

    def transform_most_expensive(self) -> None:
        """Transform and load most expensive products."""
        sql_file = os.path.join(self.sql_dir, 'transform_most_expensive.sql')
        with DatabaseConnection() as cursor:
            execute_sql_file(cursor, sql_file)
            logger.info("Most expensive products transformed successfully")

    def transform_users(self) -> None:
        """Transform and load normalized user data."""
        sql_file = os.path.join(self.sql_dir, 'transform_ods_users.sql')
        with DatabaseConnection() as cursor:
            execute_sql_file(cursor, sql_file)
            logger.info("User data transformed successfully")