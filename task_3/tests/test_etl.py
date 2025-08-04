"""Test suite for ETL process."""
import pytest
from src.extractor import FakeStoreAPI
from src.transformer import DataTransformer
from src.database import DatabaseConnection, load_db_config

def test_db_config_loading():
    """Test database configuration loading."""
    with pytest.raises(FileNotFoundError):
        load_db_config('nonexistent.ini')

def test_api_connection():
    """Test API connection."""
    api_client = FakeStoreAPI()
    try:
        products = api_client.get_products()
        assert isinstance(products, list)
        assert len(products) > 0
    except ConnectionError:
        pytest.skip("API is not available")

def test_database_connection():
    """Test database connection."""
    try:
        with DatabaseConnection() as cursor:
            assert cursor is not None
    except ConnectionError:
        pytest.skip("Database is not available")