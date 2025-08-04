"""Database connection and operations module."""
import os
import psycopg2
from configparser import ConfigParser
from typing import Dict, Any


def load_db_config(filename: str = 'database.ini', section: str = 'postgresql') -> Dict[str, Any]:
    """Load database connection parameters from config file."""
    parser = ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', filename)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {filename} not found")
    
    parser.read(config_path)

    if not parser.has_section(section):
        raise ValueError(f'Section {section} not found in {filename}')

    return {param[0]: param[1] for param in parser.items(section)}


class DatabaseConnection:
    """Database connection context manager."""
    
    def __init__(self, config_file: str = 'database.ini'):
        """Initialize database connection parameters."""
        self.config = load_db_config(config_file)
        self.conn = None
        self.cur = None

    def __enter__(self):
        """Create database connection and cursor."""
        try:
            self.conn = psycopg2.connect(**self.config)
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


def execute_sql_file(cursor, sql_file: str) -> None:
    """Execute SQL commands from a file."""
    try:
        with open(sql_file, 'r') as f:
            sql_commands = f.read()
        cursor.execute(sql_commands)
    except (psycopg2.Error, FileNotFoundError) as e:
        raise Exception(f"Failed to execute SQL file {sql_file}: {str(e)}")