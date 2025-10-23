#!/usr/bin/env python3
"""
Test script for Supermarket Sales ETL Pipeline
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / ".." / "src"))
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_extract():
    """Test data extraction"""
    print("=== Testing Data Extraction ===")
    try:
        from src.etl.extract import extract_data
        
        data = extract_data()
        print(f"✅ Extraction successful: {len(data)} records")
        print(f"Columns: {list(data.columns)}")
        print(f"Data types:\n{data.dtypes}")
        return data
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        return None

def test_transform(raw_data):
    """Test data transformation"""
    print("\n=== Testing Data Transformation ===")
    try:
        from src.etl.transform import transform_data
        
        transformed_data = transform_data(raw_data)
        print("✅ Transformation successful")
        
        for table_name, table_data in transformed_data.items():
            print(f"  {table_name}: {len(table_data)} records")
            if len(table_data) > 0:
                print(f"    Columns: {list(table_data.columns)}")
        
        return transformed_data
    except Exception as e:
        print(f"❌ Transformation failed: {str(e)}")
        return None

def test_database_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")
    try:
        from src.database.connection import test_connection
        
        if test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Supermarket Sales ETL Pipeline Test")
    print("=" * 50)
    
    # Test 1: Data Extraction
    raw_data = test_extract()
    if raw_data is None:
        print("\n❌ Cannot proceed without data extraction")
        return
    
    # Test 2: Data Transformation
    transformed_data = test_transform(raw_data)
    if transformed_data is None:
        print("\n❌ Cannot proceed without data transformation")
        return
    
    # Test 3: Database Connection
    db_ok = test_database_connection()
    if not db_ok:
        print("\n⚠️  Database connection failed. Please check your database setup.")
        print("   You can still test the ETL process without loading to database.")
    
    print("\n" + "=" * 50)
    print("🎉 ETL Pipeline Test Completed!")
    
    if db_ok:
        print("\n📋 Next steps:")
        print("1. Run: python scripts/run_etl.py")
        print("2. Check your PostgreSQL database")
        print("3. Connect PowerBI to your database")
    else:
        print("\n📋 Next steps:")
        print("1. Setup PostgreSQL database")
        print("2. Update .env file with database credentials")
        print("3. Run: python scripts/run_etl.py")

if __name__ == "__main__":
    main()
