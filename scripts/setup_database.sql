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
CREATE TABLE dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_type VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Product
CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    product_line VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Time
CREATE TABLE dim_time (
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
CREATE TABLE dim_branch (
    branch_id SERIAL PRIMARY KEY,
    branch VARCHAR(10) NOT NULL,
    city VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Payment
CREATE TABLE dim_payment (
    payment_id SERIAL PRIMARY KEY,
    payment_method VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- FACT TABLE
-- =============================================

-- Fact: Sales
CREATE TABLE fact_sales (
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
    rating DECIMAL(3,2) NOT NULL,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Indexes for fact table
CREATE INDEX idx_fact_sales_invoice_id ON fact_sales(invoice_id);
CREATE INDEX idx_fact_sales_customer_id ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product_id ON fact_sales(product_id);
CREATE INDEX idx_fact_sales_time_id ON fact_sales(time_id);
CREATE INDEX idx_fact_sales_branch_id ON fact_sales(branch_id);
CREATE INDEX idx_fact_sales_payment_id ON fact_sales(payment_id);
CREATE INDEX idx_fact_sales_date ON fact_sales(created_at);

-- Indexes for dimension tables
CREATE INDEX idx_dim_customer_type ON dim_customer(customer_type);
CREATE INDEX idx_dim_product_line ON dim_product(product_line);
CREATE INDEX idx_dim_time_date ON dim_time(date);
CREATE INDEX idx_dim_branch_city ON dim_branch(city);
CREATE INDEX idx_dim_payment_method ON dim_payment(payment_method);

-- =============================================
-- VIEWS FOR REPORTING
-- =============================================

-- View: Sales Summary
CREATE VIEW v_sales_summary AS
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
-- STORED PROCEDURES
-- =============================================

-- Procedure: Update dimension tables
CREATE OR REPLACE FUNCTION update_dimensions()
RETURNS VOID AS $$
BEGIN
    -- Update customer dimension
    INSERT INTO dim_customer (customer_type, gender)
    SELECT DISTINCT customer_type, gender
    FROM temp_sales_data
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_customer 
        WHERE customer_type = temp_sales_data.customer_type 
        AND gender = temp_sales_data.gender
    );
    
    -- Update product dimension
    INSERT INTO dim_product (product_line, unit_price)
    SELECT DISTINCT product_line, unit_price
    FROM temp_sales_data
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_product 
        WHERE product_line = temp_sales_data.product_line 
        AND unit_price = temp_sales_data.unit_price
    );
    
    -- Update time dimension
    INSERT INTO dim_time (date, time, year, month, day, quarter, weekday, is_weekend)
    SELECT DISTINCT 
        date,
        time,
        EXTRACT(YEAR FROM date),
        EXTRACT(MONTH FROM date),
        EXTRACT(DAY FROM date),
        EXTRACT(QUARTER FROM date),
        EXTRACT(DOW FROM date),
        EXTRACT(DOW FROM date) IN (0, 6)
    FROM temp_sales_data
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_time 
        WHERE dim_time.date = temp_sales_data.date 
        AND dim_time.time = temp_sales_data.time
    );
    
    -- Update branch dimension
    INSERT INTO dim_branch (branch, city)
    SELECT DISTINCT branch, city
    FROM temp_sales_data
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_branch 
        WHERE branch = temp_sales_data.branch 
        AND city = temp_sales_data.city
    );
    
    -- Update payment dimension
    INSERT INTO dim_payment (payment_method)
    SELECT DISTINCT payment
    FROM temp_sales_data
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_payment 
        WHERE payment_method = temp_sales_data.payment
    );
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- GRANTS
-- =============================================

-- Cấp quyền cho user
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO supermarket_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO supermarket_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO supermarket_user;
