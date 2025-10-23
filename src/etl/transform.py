"""
Transform module for Supermarket Sales ETL Pipeline
Handles data transformation and cleaning
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Tuple
import re
from pathlib import Path

from ..utils.logging import get_logger, log_function_call

logger = get_logger(__name__)

class DataTransformer:
    """Data transformation class"""
    
    def __init__(self):
        self.dimension_tables = {}
        self.fact_data = None
    
    @log_function_call
    def transform_data(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Transform raw data into dimensional model
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Dictionary with dimension tables and fact table
        """
        try:
            logger.info("Starting data transformation")
            
            # Clean and prepare data
            cleaned_df = self._clean_data(df)
            
            # Create dimension tables
            self._create_dimensions(cleaned_df)
            
            # Create fact table
            self._create_fact_table(cleaned_df)
            
            logger.info("Data transformation completed successfully")
            
            return {
                'dim_customer': self.dimension_tables['customer'],
                'dim_product': self.dimension_tables['product'],
                'dim_time': self.dimension_tables['time'],
                'dim_branch': self.dimension_tables['branch'],
                'dim_payment': self.dimension_tables['payment'],
                'fact_sales': self.fact_data
            }
            
        except Exception as e:
            logger.error(f"Data transformation failed: {str(e)}")
            raise
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare raw data
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data")
        
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Convert date column
        cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'])
        
        # Convert time column
        cleaned_df['Time'] = pd.to_datetime(cleaned_df['Time'], format='%I:%M:%S %p').dt.time
        
        # Clean string columns
        string_columns = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']
        for col in string_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].str.strip()
        
        # Ensure numeric columns are numeric
        numeric_columns = ['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'cogs', 'gross income', 'Rating']
        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        # Handle missing values
        cleaned_df = cleaned_df.dropna()
        
        logger.info(f"Data cleaning completed. {len(cleaned_df)} records remaining")
        return cleaned_df
    
    def _create_dimensions(self, df: pd.DataFrame) -> None:
        """
        Create dimension tables
        
        Args:
            df: Cleaned DataFrame
        """
        logger.info("Creating dimension tables")
        
        # Customer dimension
        customer_df = df[['Customer type', 'Gender']].drop_duplicates().reset_index(drop=True)
        customer_df.columns = ['customer_type', 'gender']
        customer_df.insert(0, 'customer_id', range(1, len(customer_df) + 1))
        self.dimension_tables['customer'] = customer_df
        
        # Product dimension
        product_df = df[['Product line', 'Unit price']].drop_duplicates().reset_index(drop=True)
        product_df.columns = ['product_line', 'unit_price']
        product_df.insert(0, 'product_id', range(1, len(product_df) + 1))
        self.dimension_tables['product'] = product_df
        
        # Time dimension
        time_data = []
        for _, row in df[['Date', 'Time']].drop_duplicates().iterrows():
            date = row['Date']
            time = row['Time']
            time_data.append({
                'date': date,
                'time': time,
                'year': date.year,
                'month': date.month,
                'day': date.day,
                'quarter': (date.month - 1) // 3 + 1,
                'weekday': date.weekday(),
                'is_weekend': date.weekday() >= 5
            })
        
        self.dimension_tables['time'] = pd.DataFrame(time_data)
        self.dimension_tables['time'].insert(0, 'time_id', range(1, len(self.dimension_tables['time']) + 1))
        
        # Branch dimension
        branch_df = df[['Branch', 'City']].drop_duplicates().reset_index(drop=True)
        branch_df.columns = ['branch', 'city']
        branch_df.insert(0, 'branch_id', range(1, len(branch_df) + 1))
        self.dimension_tables['branch'] = branch_df
        
        # Payment dimension
        payment_df = df[['Payment']].drop_duplicates().reset_index(drop=True)
        payment_df.columns = ['payment_method']
        payment_df.insert(0, 'payment_id', range(1, len(payment_df) + 1))
        self.dimension_tables['payment'] = payment_df
        
        logger.info("Dimension tables created successfully")
    
    def _create_fact_table(self, df: pd.DataFrame) -> None:
        """
        Create fact table with foreign keys
        
        Args:
            df: Cleaned DataFrame
        """
        logger.info("Creating fact table")
        
        # Create lookup dictionaries for foreign keys
        customer_lookup = dict(zip(
            zip(self.dimension_tables['customer']['customer_type'], 
                self.dimension_tables['customer']['gender']),
            self.dimension_tables['customer']['customer_id']
        ))
        
        product_lookup = dict(zip(
            zip(self.dimension_tables['product']['product_line'], 
                self.dimension_tables['product']['unit_price']),
            self.dimension_tables['product']['product_id']
        ))
        
        time_lookup = dict(zip(
            zip(self.dimension_tables['time']['date'], 
                self.dimension_tables['time']['time']),
            self.dimension_tables['time']['time_id']
        ))
        
        branch_lookup = dict(zip(
            zip(self.dimension_tables['branch']['branch'], 
                self.dimension_tables['branch']['city']),
            self.dimension_tables['branch']['branch_id']
        ))
        
        payment_lookup = dict(zip(
            self.dimension_tables['payment']['payment_method'],
            self.dimension_tables['payment']['payment_id']
        ))
        
        # Create fact table
        fact_data = []
        for _, row in df.iterrows():
            fact_data.append({
                'invoice_id': row['Invoice ID'],
                'customer_id': customer_lookup.get((row['Customer type'], row['Gender'])),
                'product_id': product_lookup.get((row['Product line'], row['Unit price'])),
                'time_id': time_lookup.get((row['Date'], row['Time'])),
                'branch_id': branch_lookup.get((row['Branch'], row['City'])),
                'payment_id': payment_lookup.get(row['Payment']),
                'quantity': row['Quantity'],
                'tax_5_percent': row['Tax 5%'],
                'sales': row['Sales'],
                'cogs': row['cogs'],
                'gross_margin_percentage': row['gross margin percentage'],
                'gross_income': row['gross income'],
                'rating': row['Rating']
            })
        
        self.fact_data = pd.DataFrame(fact_data)
        logger.info(f"Fact table created with {len(self.fact_data)} records")
        
        # Save processed data to files
        self._save_processed_data()
    
    def _save_processed_data(self):
        """Save processed data to processed directory"""
        try:
            # Create processed directory
            processed_dir = Path(__file__).parent.parent.parent / "data" / "processed"
            processed_dir.mkdir(parents=True, exist_ok=True)
            
            # Save dimension tables
            for table_name, table_data in self.dimension_tables.items():
                file_path = processed_dir / f"{table_name}.csv"
                table_data.to_csv(file_path, index=False)
                logger.info(f"Saved {table_name} to {file_path}")
            
            # Save fact table
            fact_file_path = processed_dir / "fact_sales.csv"
            self.fact_data.to_csv(fact_file_path, index=False)
            logger.info(f"Saved fact_sales to {fact_file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save processed data: {str(e)}")

def transform_data(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Main function to transform data
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Dictionary with transformed data
    """
    transformer = DataTransformer()
    return transformer.transform_data(df)

if __name__ == "__main__":
    # Test transformation
    from .extract import extract_data
    
    try:
        raw_data = extract_data()
        transformed_data = transform_data(raw_data)
        
        print("Transformation completed successfully!")
        for table_name, table_data in transformed_data.items():
            print(f"{table_name}: {len(table_data)} records")
            
    except Exception as e:
        print(f"Transformation failed: {str(e)}")
