import logging
import os

from dotenv import load_dotenv

load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env"),
    override=True,
)

# database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


# api settings
API_BASE_URL = os.getenv("API_BASE_URL", "https://fakestoreapi.in/api")
API_TIMEOUT = 5
API_RETRY_ATTEMPTS = 3


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)