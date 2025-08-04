"""Data transformation module."""

import os
import json
import logging
from typing import List, Dict, Any
from .database import DatabaseConnection, execute_sql_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformer:
    """Handle data transformations and database operations."""

    def __init__(self):
        """Initialize transformer with SQL scripts directory path."""
        self.sql_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "sql"
        )

    def create_tables(self) -> None:
        """Create database tables."""
        sql_file = os.path.join(self.sql_dir, "create_tables.sql")
        with DatabaseConnection() as cursor:
            execute_sql_file(cursor, sql_file)
            logger.info("Database tables created successfully")

    def load_products(self, products: List[Dict[str, Any]]) -> None:
        """Load products data into database."""
        with DatabaseConnection() as cursor:
            for product in products:
                cursor.execute(
                    """
                    INSERT INTO products (
                        id, title, price, description, image, brand, model,
                        color, category, popular, discount, on_sale
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                    """,
                    (
                        product["id"],
                        product["title"],
                        product["price"],
                        product.get("description"),
                        product.get("image"),
                        product.get("brand"),
                        product.get("model"),
                        product.get("color"),
                        product.get("category"),
                        product.get("popular", False),
                        product.get("discount"),
                        product.get("onSale", False),
                    ),
                )
            logger.info(f"Loaded {len(products)} products into database")

    def load_users(self, users: List[Dict[str, Any]]) -> None:
        """Load users data into database."""
        with DatabaseConnection() as cursor:
            for user in users:
                cursor.execute(
                    """
                    INSERT INTO users (
                        id, name, address
                    ) VALUES (
                        %s, %s, %s
                    ) ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        address = EXCLUDED.address
                    """,
                    (
                        user["id"],
                        json.dumps(user["name"]),
                        json.dumps(user["address"]),
                    ),
                )
            logger.info(f"Loaded {len(users)} users into database")

    def transform_most_expensive(self) -> None:
        """Transform and load most expensive products."""
        sql_file = os.path.join(self.sql_dir, "transform_most_expensive.sql")
        with DatabaseConnection() as cursor:
            execute_sql_file(cursor, sql_file)
            logger.info("Most expensive products transformed successfully")

    def transform_users(self) -> None:
        """Transform and load normalized user data."""
        sql_file = os.path.join(self.sql_dir, "transform_ods_users.sql")
        with DatabaseConnection() as cursor:
            execute_sql_file(cursor, sql_file)
            logger.info("User data transformed successfully")
