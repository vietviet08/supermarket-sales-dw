"""
Database connection utilities for Supermarket Sales Data Warehouse
"""

import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from typing import Optional, Dict, Any
from contextlib import contextmanager

from ..utils.config import get_database_config
from ..utils.logging import get_logger

logger = get_logger(__name__)

class DatabaseConnection:
    """Database connection manager"""
    
    def __init__(self):
        self.config = get_database_config()
        self.engine = None
        self._create_engine()
    
    def _create_engine(self):
        """Create SQLAlchemy engine"""
        try:
            connection_string = (
                f"postgresql://{self.config['user']}:{self.config['password']}"
                f"@{self.config['host']}:{self.config['port']}/{self.config['name']}"
            )
            self.engine = create_engine(connection_string)
            logger.info("Database engine created successfully")
        except Exception as e:
            logger.error(f"Failed to create database engine: {str(e)}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = None
        try:
            conn = self.engine.connect()
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Execute SQL query and return DataFrame
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            DataFrame with query results
        """
        try:
            with self.get_connection() as conn:
                df = pd.read_sql(query, conn, params=params)
                logger.info(f"Query executed successfully, returned {len(df)} rows")
                return df
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def execute_command(self, command: str, params: Optional[Dict] = None) -> None:
        """
        Execute SQL command (INSERT, UPDATE, DELETE)
        
        Args:
            command: SQL command string
            params: Command parameters
        """
        try:
            with self.get_connection() as conn:
                from sqlalchemy import text
                conn.execute(text(command), params)
                conn.commit()
                logger.info("Command executed successfully")
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            raise
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> None:
        """
        Insert DataFrame into database table
        
        Args:
            df: DataFrame to insert
            table_name: Target table name
            if_exists: What to do if table exists ('append', 'replace', 'fail')
        """
        try:
            with self.get_connection() as conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False, method='multi')
                logger.info(f"Inserted {len(df)} rows into {table_name}")
        except Exception as e:
            logger.error(f"Failed to insert DataFrame: {str(e)}")
            raise

def test_connection() -> bool:
    """
    Test database connection
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        db = DatabaseConnection()
        with db.get_connection() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1")).fetchone()
            logger.info("Database connection test successful")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False

# Global database instance
db_connection = DatabaseConnection()
