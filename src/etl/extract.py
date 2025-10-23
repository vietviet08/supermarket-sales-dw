"""
Extract module for Supermarket Sales ETL Pipeline
Handles data extraction from CSV files
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import os

from ..utils.config import get_data_paths, get_data_quality_config
from ..utils.logging import get_logger, log_function_call

logger = get_logger(__name__)

class DataExtractor:
    """Data extraction class"""
    
    def __init__(self):
        self.data_paths = get_data_paths()
        self.quality_config = get_data_quality_config()
        self.required_columns = self.quality_config['required_columns']
    
    @log_function_call
    def extract_csv(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Extract data from CSV file
        
        Args:
            file_path: Path to CSV file. If None, uses default path
            
        Returns:
            DataFrame with extracted data
        """
        if file_path is None:
            # Look for CSV files in raw data directory
            raw_path = self.data_paths['raw']
            csv_files = list(raw_path.glob("*.csv"))
            
            if not csv_files:
                raise FileNotFoundError(f"No CSV files found in {raw_path}")
            
            # Use the first CSV file found
            file_path = csv_files[0]
            logger.info(f"Using CSV file: {file_path}")
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            logger.info(f"Successfully loaded {len(df)} records from {file_path}")
            
            # Validate required columns
            self._validate_columns(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to extract data from {file_path}: {str(e)}")
            raise
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        """
        Validate that all required columns are present
        
        Args:
            df: DataFrame to validate
        """
        missing_columns = set(self.required_columns) - set(df.columns)
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logger.info("All required columns present")
    
    @log_function_call
    def extract_supermarket_data(self) -> pd.DataFrame:
        """
        Extract Supermarket Sales data specifically
        
        Returns:
            DataFrame with supermarket sales data
        """
        try:
            # Look for SuperMarketAnalysis.csv
            raw_path = self.data_paths['raw']
            csv_file = raw_path / "SuperMarketAnalysis.csv"
            
            if not csv_file.exists():
                raise FileNotFoundError(f"SuperMarketAnalysis.csv not found in {raw_path}")
            
            # Read the CSV file
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded Supermarket Sales data: {len(df)} records")
            
            # Basic data validation
            self._validate_data_quality(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to extract supermarket data: {str(e)}")
            raise
    
    def _validate_data_quality(self, df: pd.DataFrame) -> None:
        """
        Validate data quality
        
        Args:
            df: DataFrame to validate
        """
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            logger.warning(f"Found missing values: {missing_values[missing_values > 0].to_dict()}")
        
        # Check sales amount range
        if 'Sales' in df.columns:
            min_sales = df['Sales'].min()
            max_sales = df['Sales'].max()
            
            if min_sales < self.quality_config['min_sales_amount']:
                logger.warning(f"Sales amount below minimum: {min_sales}")
            
            if max_sales > self.quality_config['max_sales_amount']:
                logger.warning(f"Sales amount above maximum: {max_sales}")
        
        logger.info("Data quality validation completed")

def extract_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Main function to extract data
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        DataFrame with extracted data
    """
    extractor = DataExtractor()
    return extractor.extract_supermarket_data()

if __name__ == "__main__":
    # Test extraction
    try:
        data = extract_data()
        print(f"Extracted {len(data)} records")
        print(f"Columns: {list(data.columns)}")
        print(f"First few rows:\n{data.head()}")
    except Exception as e:
        print(f"Extraction failed: {str(e)}")
