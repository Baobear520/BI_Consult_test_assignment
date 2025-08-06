"""Database connection and operations module."""

from typing import Dict, Any, Optional, List
import logging

import psycopg2

from task_3.config.utils import check_db_config
from task_3.src.interfaces import DatabaseDriver


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgresDriver(DatabaseDriver):
    """Database connection context manager."""

    def __init__(self, config: Dict[str, Any] = check_db_config()):
        super().__init__(config)

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
    









