"""
Load module for Supermarket Sales ETL Pipeline
Handles data loading into PostgreSQL data warehouse
"""

import pandas as pd
from typing import Dict, Any
from pathlib import Path

from ..database.connection import db_connection
from ..utils.logging import get_logger, log_function_call

logger = get_logger(__name__)

class DataLoader:
    """Data loading class"""
    
    def __init__(self):
        self.db = db_connection
    
    @log_function_call
    def load_data(self, transformed_data: Dict[str, pd.DataFrame]) -> None:
        """
        Load transformed data into data warehouse
        
        Args:
            transformed_data: Dictionary with dimension and fact tables
        """
        try:
            logger.info("Starting data loading process")
            
            # Clear fact table first to avoid FK constraint violations
            self._clear_table('fact_sales')
            
            # Load dimension tables first
            self._load_dimensions(transformed_data)
            
            # Load fact table
            self._load_fact_table(transformed_data)
            
            logger.info("Data loading completed successfully")
            
            # Export data warehouse to files
            self._export_warehouse_data()
            
        except Exception as e:
            logger.error(f"Data loading failed: {str(e)}")
            raise
    
    def _load_dimensions(self, data: Dict[str, pd.DataFrame]) -> None:
        """
        Load dimension tables
        
        Args:
            data: Dictionary with transformed data
        """
        logger.info("Loading dimension tables")
        
        dimension_tables = [
            'dim_customer', 'dim_product', 'dim_time', 
            'dim_branch', 'dim_payment'
        ]
        
        for table_name in dimension_tables:
            if table_name in data:
                try:
                    # Clear existing data (for development)
                    self._clear_table(table_name)
                    
                    # Insert new data
                    self.db.insert_dataframe(
                        data[table_name], 
                        table_name, 
                        if_exists='append'
                    )
                    
                    logger.info(f"Loaded {len(data[table_name])} records into {table_name}")
                    
                except Exception as e:
                    logger.error(f"Failed to load {table_name}: {str(e)}")
                    raise
    
    def _load_fact_table(self, data: Dict[str, pd.DataFrame]) -> None:
        """
        Load fact table
        
        Args:
            data: Dictionary with transformed data
        """
        logger.info("Loading fact table")
        
        if 'fact_sales' in data:
            try:
                # Note: fact_sales is already cleared in load_data() to avoid FK constraints
                
                # Insert data in batches to avoid parameter limit
                batch_size = 50
                df = data['fact_sales']
                total_records = len(df)
                
                for i in range(0, total_records, batch_size):
                    batch_df = df.iloc[i:i+batch_size]
                    self.db.insert_dataframe(
                        batch_df, 
                        'fact_sales', 
                        if_exists='append'
                    )
                    logger.info(f"Loaded batch {i//batch_size + 1}: {len(batch_df)} records")
                
                logger.info(f"Loaded {total_records} records into fact_sales")
                
            except Exception as e:
                logger.error(f"Failed to load fact_sales: {str(e)}")
                raise
    
    def _export_warehouse_data(self):
        """Export data warehouse to files for PowerBI and analysis"""
        try:
            # Create warehouse directory
            warehouse_dir = Path(__file__).parent.parent.parent / "data" / "warehouse"
            warehouse_dir.mkdir(parents=True, exist_ok=True)
            
            # Export sales summary view (main export for PowerBI)
            sales_summary = self.db.execute_query("SELECT * FROM v_sales_summary")
            sales_summary_file = warehouse_dir / "sales_summary.csv"
            sales_summary.to_csv(sales_summary_file, index=False)
            logger.info(f"Exported sales summary to {sales_summary_file}")
            
            # Export individual dimension tables
            dimension_tables = ['dim_customer', 'dim_product', 'dim_time', 'dim_branch', 'dim_payment']
            for table in dimension_tables:
                try:
                    data = self.db.execute_query(f"SELECT * FROM {table}")
                    file_path = warehouse_dir / f"{table}.csv"
                    data.to_csv(file_path, index=False)
                    logger.info(f"Exported {table} to {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to export {table}: {str(e)}")
            
            # Export fact table
            try:
                fact_data = self.db.execute_query("SELECT * FROM fact_sales")
                fact_file = warehouse_dir / "fact_sales.csv"
                fact_data.to_csv(fact_file, index=False)
                logger.info(f"Exported fact_sales to {fact_file}")
            except Exception as e:
                logger.warning(f"Failed to export fact_sales: {str(e)}")
            
            # Create PowerBI ready export
            self._create_powerbi_export(warehouse_dir)
            
        except Exception as e:
            logger.error(f"Failed to export warehouse data: {str(e)}")
    
    def _create_powerbi_export(self, warehouse_dir: Path):
        """Create PowerBI ready exports with specific queries"""
        try:
            # Sales by branch and city
            branch_sales = self.db.execute_query("""
                SELECT branch, city, 
                       SUM(sales) as total_sales,
                       COUNT(*) as transaction_count,
                       AVG(sales) as avg_sales
                FROM v_sales_summary 
                GROUP BY branch, city
                ORDER BY total_sales DESC
            """)
            branch_sales.to_csv(warehouse_dir / "sales_by_branch.csv", index=False)
            
            # Sales by product line
            product_sales = self.db.execute_query("""
                SELECT product_line,
                       SUM(sales) as total_sales,
                       COUNT(*) as transaction_count,
                       AVG(unit_price) as avg_unit_price
                FROM v_sales_summary 
                GROUP BY product_line
                ORDER BY total_sales DESC
            """)
            product_sales.to_csv(warehouse_dir / "sales_by_product.csv", index=False)
            
            # Monthly sales trend
            monthly_sales = self.db.execute_query("""
                SELECT year, month,
                       SUM(sales) as total_sales,
                       COUNT(*) as transaction_count
                FROM v_sales_summary 
                GROUP BY year, month
                ORDER BY year, month
            """)
            monthly_sales.to_csv(warehouse_dir / "monthly_sales_trend.csv", index=False)
            
            # Customer analysis
            customer_analysis = self.db.execute_query("""
                SELECT customer_type, gender,
                       SUM(sales) as total_sales,
                       COUNT(*) as transaction_count,
                       AVG(rating) as avg_rating
                FROM v_sales_summary 
                GROUP BY customer_type, gender
                ORDER BY total_sales DESC
            """)
            customer_analysis.to_csv(warehouse_dir / "customer_analysis.csv", index=False)
            
            logger.info("Created PowerBI ready exports")
            
        except Exception as e:
            logger.error(f"Failed to create PowerBI exports: {str(e)}")
    
    def _clear_table(self, table_name: str) -> None:
        """
        Clear table data (for development purposes)
        
        Args:
            table_name: Name of table to clear
        """
        try:
            # Only clear if it's a development environment
            # In production, you might want to append or update instead
            self.db.execute_command(f"DELETE FROM {table_name}")
            logger.info(f"Cleared table {table_name}")
        except Exception as e:
            logger.warning(f"Could not clear table {table_name}: {str(e)}")
    
    @log_function_call
    def validate_data_warehouse(self) -> Dict[str, int]:
        """
        Validate data warehouse after loading
        
        Returns:
            Dictionary with record counts for each table
        """
        logger.info("Validating data warehouse")
        
        tables = [
            'dim_customer', 'dim_product', 'dim_time',
            'dim_branch', 'dim_payment', 'fact_sales'
        ]
        
        record_counts = {}
        
        for table in tables:
            try:
                result = self.db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                count = result['count'].iloc[0]
                record_counts[table] = count
                logger.info(f"{table}: {count} records")
            except Exception as e:
                logger.error(f"Failed to validate {table}: {str(e)}")
                record_counts[table] = 0
        
        return record_counts
    
    @log_function_call
    def create_summary_report(self) -> pd.DataFrame:
        """
        Create summary report of loaded data
        
        Returns:
            DataFrame with summary statistics
        """
        try:
            query = """
            SELECT 
                dc.customer_type,
                dc.gender,
                dp.product_line,
                db.branch,
                db.city,
                dpm.payment_method,
                COUNT(*) as transaction_count,
                SUM(fs.sales) as total_sales,
                AVG(fs.rating) as avg_rating
            FROM fact_sales fs
            JOIN dim_customer dc ON fs.customer_id = dc.customer_id
            JOIN dim_product dp ON fs.product_id = dp.product_id
            JOIN dim_branch db ON fs.branch_id = db.branch_id
            JOIN dim_payment dpm ON fs.payment_id = dpm.payment_id
            GROUP BY dc.customer_type, dc.gender, dp.product_line, 
                     db.branch, db.city, dpm.payment_method
            ORDER BY total_sales DESC
            """
            
            summary = self.db.execute_query(query)
            logger.info(f"Created summary report with {len(summary)} rows")
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to create summary report: {str(e)}")
            raise

def load_data(transformed_data: Dict[str, pd.DataFrame]) -> None:
    """
    Main function to load data
    
    Args:
        transformed_data: Dictionary with transformed data
    """
    loader = DataLoader()
    loader.load_data(transformed_data)

if __name__ == "__main__":
    # Test loading
    from .extract import extract_data
    from .transform import transform_data
    
    try:
        # Extract and transform data
        raw_data = extract_data()
        transformed_data = transform_data(raw_data)
        
        # Load data
        load_data(transformed_data)
        
        # Validate
        loader = DataLoader()
        record_counts = loader.validate_data_warehouse()
        print("Data warehouse validation:")
        for table, count in record_counts.items():
            print(f"  {table}: {count} records")
        
        # Create summary report
        summary = loader.create_summary_report()
        print(f"\nSummary report created with {len(summary)} rows")
        
    except Exception as e:
        print(f"Loading failed: {str(e)}")
