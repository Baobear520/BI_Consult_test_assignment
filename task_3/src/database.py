"""Database connection and operations module."""

from abc import abstractmethod
from typing import List
import os

import psycopg2
from typing import Dict, Any, Optional
import logging
from ..config.settings import DB_CONFIG


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseDriver:
    """Database connection context manager."""

    def __init__(self):
        """Initialize database connection parameters."""
        self.config = self.__check_db_config()
        self.conn = None
        self.cur = None
    
    def __check_db_config(self) -> Dict[str, Any]:
        """Load database connection parameters from environment variables."""
        required_params = ("host", "port", "dbname", "user", "password")
        missing_params = [
            param for param in required_params if param not in DB_CONFIG
        ]
        if missing_params:
            raise ValueError(
                f"Missing required database parameters: {', '.join(missing_params)}"
                f"Please check your environment variables."
            )

        return DB_CONFIG

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
            logger.error("Failed to connect to database: %s", str(e))
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    def __enter__(self):
        """Create database connection and cursor."""
        try:
            self.conn = self.__get_connection()
            self.cur = self.conn.cursor()
            return self.cur
        except psycopg2.Error as e:
            logger.error("Failed to connect to database: %s", str(e))
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

    def execute_sql_file(
        self,
        sql_file: str,
        many: bool = False,
        params: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None
    ) -> None:

        """Execute SQL commands from a file."""
        try:
            with self as cursor:
                with open(sql_file, "r") as f:
                    sql_commands = f.read()
                if params and many:
                    cursor.executemany(sql_commands, params)
                elif params:
                    cursor.execute(sql_commands, params)
                else:
                    cursor.execute(sql_commands)
                logger.info("SQL file %s executed successfully", sql_file)
        except (psycopg2.Error, FileNotFoundError) as e:
            logger.error("Failed to execute SQL file %s: %s", sql_file, str(e))
            raise Exception(f"Failed to execute SQL file {sql_file}: {str(e)}")
    









