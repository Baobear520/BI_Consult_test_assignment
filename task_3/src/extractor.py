"""Data extraction module for FakeStore API."""

import os
import requests
from typing import Dict, List, Any
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env"),
    override=True,
)


class FakeStoreAPI:
    """FakeStore API client."""

    def __init__(self):
        """Initialize and configure API client."""

        self.base_url = os.getenv("API_BASE_URL", "https://fakestoreapi.in/api")
        self.timeout = int(os.getenv("API_TIMEOUT", "5"))
        self.retry_attempts = int(os.getenv("API_RETRY_ATTEMPTS", "3"))

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make HTTP request to the API."""
        for attempt in range(self.retry_attempts):
            try:
                response = requests.get(
                    f"{self.base_url}{endpoint}", timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                if attempt == self.retry_attempts - 1:  # Last attempt
                    logger.error(
                        f"Max retries reached."
                        f"API request failed after {self.retry_attempts} "
                        f"attempts: {str(e)}"
                    )
                    raise ConnectionError(
                        f"Failed to fetch data from {endpoint}: {str(e)}"
                    )
                logger.warning(
                    f"API request attempt {attempt + 1} failed, retrying..."
                )

    def get_products(self) -> List[Dict[str, Any]]:
        """Fetch products data from the API."""
        try:
            response = self._make_request("/products")
            if response["status"] != "SUCCESS":
                raise ValueError(
                    f"API returned error status: {response['status']}"
                )

            products = response["products"]
            logger.info(f"Successfully fetched {len(products)} products")
            return products
        except Exception as e:
            logger.error(f"Failed to fetch products: {str(e)}")
            raise

    def get_users(self) -> List[Dict[str, Any]]:
        """Fetch users data from the API."""
        try:
            response = self._make_request("/users")
            if response["status"] != "SUCCESS":
                raise ValueError(f"API returned error status: {response['status']}")

            users = response["users"]
            logger.info(f"Successfully fetched {len(users)} users")
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            raise
