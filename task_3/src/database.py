"""Database connection and operations module."""

from abc import abstractmethod
from typing import List
import os

import psycopg2
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv
from ..config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env"),
    override=True,
)

class DatabaseDriver:
    """Database connection context manager."""

    def __init__(self):
        """Initialize database connection parameters."""
        self.config = self.__get_db_config()
        self.conn = None
        self.cur = None
    
    def __get_db_config(self) -> Dict[str, Any]:
        """Load database connection parameters from environment variables."""
        required_params = (
            "DB_HOST",
            "DB_PORT",
            "DB_NAME",
            "DB_USER",
        )   
        missing_params = [
            param for param in required_params if not os.getenv(param)
        ]
        if missing_params:
            raise ValueError(
                f"Missing required database parameters: {', '.join(missing_params)}"
            )

        return {
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
        }

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class PostgresDriver(DatabaseDriver):
    """Database connection context manager."""

    def __init__(self):
        super().__init__()

    def __get_connection(self):
        """Get database connection."""
        try:
            return psycopg2.connect(**self.config)
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    def __enter__(self):
        """Create database connection and cursor."""
        try:
            self.conn = self.__get_connection()
            self.cur = self.conn.cursor()
            return self.cur
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection and cursor."""
        if exc_type is not None:
            if self.conn:
                self.conn.rollback()
        else:
            if self.conn:
                self.conn.commit()

        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def execute_sql_file(self, sql_file: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Execute SQL commands from a file."""
        try:
            with self as cursor:
                with open(sql_file, "r") as f:
                    sql_commands = f.read()
                if params:
                    cursor.execute(sql_commands, params)
                else:
                    cursor.execute(sql_commands)
        except (psycopg2.Error, FileNotFoundError) as e:
            raise Exception(f"Failed to execute SQL file {sql_file}: {str(e)}")
    
    def execute_sql_file_many(self, sql_file: str, params_list: List[Dict[str, Any]]) -> None:
        """
        Execute SQL commands from a file with multiple sets of parameters.
        
        Args:
            cursor: Database cursor
            sql_file: Path to the SQL file
            params_list: List of parameter dictionaries for batch execution
        """
        try:
            with self as cursor:
                with open(sql_file, "r") as f:
                    sql_command = f.read()
                cursor.executemany(sql_command, params_list)
        except (psycopg2.Error, FileNotFoundError) as e:
            raise Exception(f"Failed to execute SQL file {sql_file}: {str(e)}")








