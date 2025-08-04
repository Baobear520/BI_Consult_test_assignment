"""Data extraction module for FakeStore API."""
import requests
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FakeStoreAPI:
    """FakeStore API client."""
    
    BASE_URL = "https://fakestoreapi.in/api"
    
    @staticmethod
    def _make_request(endpoint: str) -> Dict[str, Any]:
        """Make HTTP request to the API."""
        try:
            response = requests.get(f"{FakeStoreAPI.BASE_URL}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise ConnectionError(f"Failed to fetch data from {endpoint}: {str(e)}")

    @classmethod
    def get_products(cls) -> List[Dict[str, Any]]:
        """Fetch products data from the API."""
        try:
            response = cls._make_request("/products")
            if response["status"] != "SUCCESS":
                raise ValueError(f"API returned error status: {response['status']}")
            
            products = response["products"]
            logger.info(f"Successfully fetched {len(products)} products")
            return products
        except Exception as e:
            logger.error(f"Failed to fetch products: {str(e)}")
            raise

    @classmethod
    def get_users(cls) -> List[Dict[str, Any]]:
        """Fetch users data from the API."""
        try:
            response = cls._make_request("/users")
            if response["status"] != "SUCCESS":
                raise ValueError(f"API returned error status: {response['status']}")
            
            users = response["users"]
            logger.info(f"Successfully fetched {len(users)} users")
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            raise