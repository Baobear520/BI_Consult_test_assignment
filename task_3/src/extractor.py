"""Data extraction module for FakeStore API."""

from abc import ABC, abstractmethod
import os
import requests
from typing import Dict, List, Any
import logging
from dotenv import load_dotenv

from ..config.settings import API_BASE_URL, API_TIMEOUT, API_RETRY_ATTEMPTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env"),
    override=True,
)


class APIClient(ABC):
    """Base API class."""

    def __init__(self, session: requests.Session, base_url: str, timeout: int, retry_attempts: int):
        self.base_url = base_url
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.session = session

    @abstractmethod
    def _make_request(self, endpoint: str):
        pass

            

class FakeStoreAPI(APIClient):
    """FakeStore API client."""

    ENDPOINTS = {
        "users": "/users",
        "products": "/products"
    }

    def __init__(self, session: requests.Session = requests.Session):
        super().__init__(session, API_BASE_URL, API_TIMEOUT, API_RETRY_ATTEMPTS)

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make HTTP request to the API."""
        for attempt in range(self.retry_attempts):
            try:
                response = self.session().get(
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

    def fetch_data(self, category: str) -> List[Dict[str, Any]]:
        """Fetch users data from the API."""
        try:
            if category not in self.ENDPOINTS:
                raise ValueError(f"Invalid category: {category}")

            response = self._make_request(self.ENDPOINTS[category])
            if response["status"] != "SUCCESS":
                raise ValueError(f"API returned error status: {response['status']}")

            data = response[category]
            logger.info(f"Successfully fetched {len(data)} {category} data")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch {category} data: {str(e)}")
            raise
                
