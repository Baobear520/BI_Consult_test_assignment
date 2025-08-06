
from abc import ABC, abstractmethod
import os
from typing import Any, Dict

import requests


class APIClient(ABC):
    """Base API class."""

    def __init__(
        self, 
        session: requests.Session, 
        base_url: str, 
        timeout: int, 
        retry_attempts: int
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.session = session

    @abstractmethod
    def _make_request(self, endpoint: str):
        pass


class DatabaseDriver:
    """Database connection context manager."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize database connection parameters."""
        self.config = config
        self.conn = None
        self.cur = None


    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    

class SQLDataTransformer(ABC):
    """Handle data transformations and database operations."""

    def __init__(self, db_driver: DatabaseDriver):
        """Initialize transformer with SQL scripts directory path."""
        self.sql_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), "sql"
        )
        self.db_driver = db_driver
    
    def _get_sql_path(self, filename: str) -> str:
        """Get full path to SQL file."""
        return os.path.join(self.sql_dir, filename)

class ETLProcess:
    def __init__(self, api_client: APIClient, db_driver: DatabaseDriver, transformer: SQLDataTransformer):
        self.api_client = api_client
        self.db_driver = db_driver
        self.transformer = transformer

    @abstractmethod
    def prepare(self):
        """Prepare the ETL process."""
        pass

    @abstractmethod
    def extract(self):
        """Extract the data."""
        pass

    @abstractmethod
    def load(self, data):
        """Load the data."""
        pass
    
    @abstractmethod
    def transform(self):
        """Transform the data."""
        pass

    def run(self):
        """Run the ETL process."""
        self.prepare()
        data = self.extract()
        self.load(data)
        self.transform()
