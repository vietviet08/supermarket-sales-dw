-- Supermarket Sales Data Warehouse Database Schema
-- Tạo database schema cho dự án Supermarket Sales

-- Tạo database (chạy với quyền superuser)
-- CREATE DATABASE supermarket_sales;

-- Kết nối đến database supermarket_sales
-- \c supermarket_sales;

-- Tạo extension nếu cần
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- DIMENSION TABLES
-- =============================================

-- Dimension: Customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_type VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS dim_product (
    product_id SERIAL PRIMARY KEY,
    product_line VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Time
CREATE TABLE IF NOT EXISTS dim_time (
    time_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    weekday INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Branch
CREATE TABLE IF NOT EXISTS dim_branch (
    branch_id SERIAL PRIMARY KEY,
    branch VARCHAR(10) NOT NULL,
    city VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Payment
CREATE TABLE IF NOT EXISTS dim_payment (
    payment_id SERIAL PRIMARY KEY,
    payment_method VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- FACT TABLE
-- =============================================

-- Fact: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id SERIAL PRIMARY KEY,
    invoice_id VARCHAR(50) NOT NULL UNIQUE,
    
    -- Foreign Keys
    customer_id INTEGER REFERENCES dim_customer(customer_id),
    product_id INTEGER REFERENCES dim_product(product_id),
    time_id INTEGER REFERENCES dim_time(time_id),
    branch_id INTEGER REFERENCES dim_branch(branch_id),
    payment_id INTEGER REFERENCES dim_payment(payment_id),
    
    -- Sales Metrics
    quantity INTEGER NOT NULL,
    tax_5_percent DECIMAL(10,2) NOT NULL,
    sales DECIMAL(10,2) NOT NULL,
    cogs DECIMAL(10,2) NOT NULL,
    gross_margin_percentage DECIMAL(10,2) NOT NULL,
    gross_income DECIMAL(10,2) NOT NULL,
    rating DECIMAL(4,2) NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Indexes for fact table
CREATE INDEX IF NOT EXISTS idx_fact_sales_invoice_id ON fact_sales(invoice_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_id ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product_id ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_time_id ON fact_sales(time_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_branch_id ON fact_sales(branch_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_payment_id ON fact_sales(payment_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(created_at);

-- Indexes for dimension tables
CREATE INDEX IF NOT EXISTS idx_dim_customer_type ON dim_customer(customer_type);
CREATE INDEX IF NOT EXISTS idx_dim_product_line ON dim_product(product_line);
CREATE INDEX IF NOT EXISTS idx_dim_time_date ON dim_time(date);
CREATE INDEX IF NOT EXISTS idx_dim_branch_city ON dim_branch(city);
CREATE INDEX IF NOT EXISTS idx_dim_payment_method ON dim_payment(payment_method);

-- =============================================
-- VIEWS FOR REPORTING
-- =============================================

-- View: Sales Summary
CREATE OR REPLACE VIEW v_sales_summary AS
SELECT 
    fs.invoice_id,
    dc.customer_type,
    dc.gender,
    dp.product_line,
    dp.unit_price,
    dt.date,
    dt.time,
    dt.year,
    dt.month,
    dt.quarter,
    db.branch,
    db.city,
    dpm.payment_method,
    fs.quantity,
    fs.tax_5_percent,
    fs.sales,
    fs.cogs,
    fs.gross_margin_percentage,
    fs.gross_income,
    fs.rating
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_id = dc.customer_id
JOIN dim_product dp ON fs.product_id = dp.product_id
JOIN dim_time dt ON fs.time_id = dt.time_id
JOIN dim_branch db ON fs.branch_id = db.branch_id
JOIN dim_payment dpm ON fs.payment_id = dpm.payment_id;

-- =============================================
-- GRANTS (Optional)
-- =============================================

-- Uncomment and modify these if you want to grant privileges to a specific user
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO supermarket_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO supermarket_user;
