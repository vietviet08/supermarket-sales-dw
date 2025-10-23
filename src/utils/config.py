"""
Configuration utilities for Supermarket Sales Data Warehouse
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file. If None, uses default config.yaml
        
    Returns:
        Dictionary containing configuration
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    return config

def get_database_config() -> Dict[str, str]:
    """
    Get database configuration from environment variables or config file
    
    Returns:
        Dictionary with database connection parameters
    """
    config = load_config()
    db_config = config['database']
    
    # Override with environment variables if available
    return {
        'host': os.getenv('DB_HOST', db_config['host']),
        'port': int(os.getenv('DB_PORT', db_config['port'])),
        'name': os.getenv('DB_NAME', db_config['name']),
        'user': os.getenv('DB_USER', db_config['user']),
        'password': os.getenv('DB_PASSWORD', db_config['password'])
    }

def get_data_paths() -> Dict[str, Path]:
    """
    Get data paths configuration
    
    Returns:
        Dictionary with data paths
    """
    config = load_config()
    base_path = Path(__file__).parent.parent.parent
    
    return {
        'raw': base_path / config['data_paths']['raw'],
        'processed': base_path / config['data_paths']['processed'],
        'warehouse': base_path / config['data_paths']['warehouse']
    }

def get_etl_config() -> Dict[str, Any]:
    """
    Get ETL configuration
    
    Returns:
        Dictionary with ETL parameters
    """
    config = load_config()
    return config['etl']

def get_data_quality_config() -> Dict[str, Any]:
    """
    Get data quality configuration
    
    Returns:
        Dictionary with data quality parameters
    """
    config = load_config()
    return config['data_quality']
