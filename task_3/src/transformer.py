"""Data transformation module."""

import json
import logging
from typing import List, Dict, Any, Optional

from task_3.src.interfaces import SQLDataTransformer
from task_3.src.interfaces import DatabaseDriver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FakeStoreDataTransformer(SQLDataTransformer):
    """Handle data transformations and database operations."""

    def __init__(self, db_driver: DatabaseDriver):
        super().__init__(db_driver)
    
    def run_sql_file(
        self, 
        sql_file: str, 
        many: bool = False, 
        params: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None
    ):
        """Run SQL file."""
        sql_file = self._get_sql_path(sql_file)
        self.db_driver.execute_sql_file(sql_file, many, params)
        logger.info("Running SQL file %s completed", sql_file)
    
    
    def load_products(self, sql_file: str, data: List[Dict[str, Any]]):
        """Load products into the database."""
        # Transform data to match SQL parameters
        prepared_data = [
            {
                "id": product["id"],
                "title": product["title"],
                "price": product["price"],
                "description": product.get("description"),
                "image": product.get("image"),
                "brand": product.get("brand"),
                "model": product.get("model"),
                "color": product.get("color"),
                "category": product.get("category"),
                "popular": product.get("popular", False),
                "discount": product.get("discount"),
                "on_sale": product.get("onSale", False),
            }
            for product in data
        ]
        
        self.run_sql_file(sql_file, many=True, params=prepared_data)
        logger.info("Loaded %s products successfully", len(data))

    def load_users(self, sql_file: str, data: List[Dict[str, Any]]):
        """Load users into the database."""
        # Transform data to match SQL parameters
        prepared_data = [
            {
                "id": user["id"],
                "name": json.dumps(user["name"]),
                "address": json.dumps(user["address"]),
            }
            for user in data
        ]
        
        self.run_sql_file(sql_file, many=True, params=prepared_data)
        logger.info("Loaded %s users successfully", len(data))
    



    
    

   





