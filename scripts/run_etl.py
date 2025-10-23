#!/usr/bin/env python3
"""
Supermarket Sales ETL Pipeline Runner
Chạy toàn bộ quy trình ETL cho dự án Supermarket Sales Data Warehouse
"""

import sys
import os
import logging
from pathlib import Path

# Thêm src vào Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.etl.extract import extract_data
from src.etl.transform import transform_data
from src.etl.load import load_data
from src.utils.logging import setup_logging
from src.utils.config import load_config

def main():
    """Main ETL pipeline function"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("=== Bắt đầu ETL Pipeline ===")
        
        # Load configuration
        config = load_config()
        logger.info("Đã load configuration thành công")
        
        # Step 1: Extract
        logger.info("Bước 1: Extract dữ liệu từ CSV")
        raw_data = extract_data()
        logger.info(f"Đã extract {len(raw_data)} records")
        
        # Step 2: Transform
        logger.info("Bước 2: Transform dữ liệu")
        transformed_data = transform_data(raw_data)
        logger.info(f"Đã transform {len(transformed_data)} records")
        
        # Step 3: Load
        logger.info("Bước 3: Load dữ liệu vào Data Warehouse")
        load_data(transformed_data)
        logger.info("Đã load dữ liệu thành công")
        
        logger.info("=== ETL Pipeline hoàn thành thành công ===")
        
    except Exception as e:
        logger.error(f"Lỗi trong ETL Pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()
