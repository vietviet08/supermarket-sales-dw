#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Database Setup Script for Supermarket Sales Data Warehouse
Executes the setup_database.sql file to create the database schema
This version can be run independently without the project structure
"""

import os
import sys
import psycopg2
from pathlib import Path

# Fix encoding for Windows console to support Unicode characters (emojis)
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def get_database_config():
    """
    Get database configuration
    You can modify these values according to your PostgreSQL setup
    """
    return {
        'host': 'localhost',
        'port': 5432,
        'name': 'supermarket_sales',
        'user': 'postgres',
        'password': 'root'
    }

def read_sql_file(file_path: str) -> str:
    """
    Read SQL file content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"✅ Successfully read SQL file: {file_path}")
        return content
    except Exception as e:
        print(f"❌ Failed to read SQL file {file_path}: {str(e)}")
        raise

def split_sql_statements(sql_content: str) -> list:
    """
    Smart SQL statement splitter that handles dollar-quoted strings, comments, and multi-line statements
    """
    statements = []
    current_statement = []
    in_dollar_quote = False
    dollar_tag = None
    in_single_quote = False
    in_comment = False
    
    lines = sql_content.split('\n')
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines and SQL comments at the start
        if not stripped or stripped.startswith('--'):
            continue
        
        # Check for dollar-quoted strings (used in stored procedures)
        i = 0
        while i < len(line):
            # Handle dollar quotes
            if not in_single_quote and not in_comment:
                if line[i:i+2] == '$$':
                    if not in_dollar_quote:
                        in_dollar_quote = True
                        dollar_tag = '$$'
                        i += 2
                        continue
                    elif dollar_tag == '$$':
                        in_dollar_quote = False
                        dollar_tag = None
                        i += 2
                        continue
            
            # Handle single quotes
            if not in_dollar_quote and not in_comment:
                if line[i] == "'":
                    if i > 0 and line[i-1] == '\\':
                        pass  # Escaped quote
                    else:
                        in_single_quote = not in_single_quote
            
            i += 1
        
        # Add line to current statement
        current_statement.append(line)
        
        # Check if statement is complete (ends with semicolon outside quotes)
        if not in_dollar_quote and not in_single_quote and stripped.endswith(';'):
            stmt = '\n'.join(current_statement).strip()
            if stmt and stmt != ';':
                statements.append(stmt)
            current_statement = []
    
    # Add any remaining statement
    if current_statement:
        stmt = '\n'.join(current_statement).strip()
        if stmt and stmt != ';':
            statements.append(stmt)
    
    return statements

def execute_sql_script(sql_content: str, db_config: dict) -> bool:
    """
    Execute SQL script using psycopg2
    """
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['name'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        # Set autocommit to True for DDL statements
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Smart split SQL content into statements
        statements = split_sql_statements(sql_content)
        
        print(f"📋 Executing {len(statements)} SQL statements...")
        
        successful = 0
        failed = 0
        
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    cursor.execute(statement)
                    successful += 1
                    print(f"✅ Statement {i}/{len(statements)} executed successfully")
                except Exception as e:
                    failed += 1
                    # Show first 100 chars of failed statement for debugging
                    stmt_preview = statement[:100].replace('\n', ' ')
                    print(f"⚠️ Statement {i} failed: {str(e)}")
                    print(f"   Statement preview: {stmt_preview}...")
                    # Continue with other statements
                    continue
        
        print(f"\n📊 Execution Summary: {successful} succeeded, {failed} failed")
        print("🎉 Database setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def check_database_exists(db_config: dict) -> bool:
    """
    Check if the database exists
    """
    try:
        # Connect to default postgres database to check if our database exists
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database='postgres',  # Connect to default postgres database
            user=db_config['user'],
            password=db_config['password']
        )
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_config['name'],)
        )
        
        exists = cursor.fetchone() is not None
        conn.close()
        
        return exists
        
    except Exception as e:
        print(f"❌ Failed to check database existence: {str(e)}")
        return False

def create_database_if_not_exists(db_config: dict) -> bool:
    """
    Create database if it doesn't exist
    """
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database='postgres',
            user=db_config['user'],
            password=db_config['password']
        )
        
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE {db_config['name']}")
        print(f"✅ Database '{db_config['name']}' created successfully")
        
        conn.close()
        return True
        
    except psycopg2.errors.DuplicateDatabase:
        print(f"📋 Database '{db_config['name']}' already exists")
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {str(e)}")
        return False

def main():
    """
    Main function to setup database
    """
    print("🚀 Starting Database Setup for Supermarket Sales Data Warehouse")
    print("=" * 60)
    
    try:
        # Get database configuration
        db_config = get_database_config()
        print(f"📋 Using database: {db_config['name']} on {db_config['host']}:{db_config['port']}")
        
        # Check if database exists, create if not
        if not check_database_exists(db_config):
            print("📋 Database doesn't exist, creating...")
            if not create_database_if_not_exists(db_config):
                print("❌ Failed to create database")
                return False
        else:
            print("✅ Database already exists")
        
        # Read SQL file
        current_dir = Path(__file__).parent
        sql_file_path = current_dir / "setup_database.sql"
        if not sql_file_path.exists():
            print(f"❌ SQL file not found: {sql_file_path}")
            return False
        
        sql_content = read_sql_file(str(sql_file_path))
        
        # Execute SQL script
        if execute_sql_script(sql_content, db_config):
            print("\n" + "=" * 60)
            print("🎉 Database setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Run: python scripts/run_etl.py")
            print("2. Check your PostgreSQL database")
            print("3. Connect PowerBI to your database")
            return True
        else:
            print("\n❌ Database setup failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
