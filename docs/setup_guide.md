# 🚀 Hướng dẫn Setup Supermarket Sales Data Warehouse

## ✅ Trạng thái hiện tại

-   ✅ **Cấu trúc dự án**: Hoàn thành
-   ✅ **ETL Pipeline**: Hoạt động tốt (1000 records processed)
-   ✅ **Dependencies**: Đã cài đặt thành công
-   ⚠️ **Database**: Cần setup PostgreSQL

## 📋 Các bước tiếp theo

### 1. Setup PostgreSQL Database

#### **Cài đặt PostgreSQL:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Hoặc sử dụng Docker
docker run --name postgres-supermarket \
  -e POSTGRES_DB=supermarket_sales \
  -e POSTGRES_USER=supermarket_user \
  -e POSTGRES_PASSWORD=supermarket_pass \
  -p 5432:5432 \
  -d postgres:15
```

#### **Tạo database và user:**

```bash
# Đăng nhập PostgreSQL
sudo -u postgres psql

# Tạo database
CREATE DATABASE supermarket_sales;

# Tạo user
CREATE USER supermarket_user WITH PASSWORD 'supermarket_pass';

# Cấp quyền
GRANT ALL PRIVILEGES ON DATABASE supermarket_sales TO supermarket_user;
\q
```

### 2. Cấu hình Environment

#### **Cập nhật file .env:**

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=supermarket_sales
DB_USER=supermarket_user
DB_PASSWORD=supermarket_pass

# Data Paths
RAW_DATA_PATH=./data/raw/
PROCESSED_DATA_PATH=./data/processed/
WAREHOUSE_DATA_PATH=./data/warehouse/

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/etl.log

# ETL Configuration
BATCH_SIZE=1000
MAX_RETRIES=3
```

### 3. Chạy ETL Pipeline

#### **Setup database schema:**

```bash
# Kết nối và chạy SQL script
psql -h localhost -U supermarket_user -d supermarket_sales -f scripts/setup_database.sql
```

#### **Chạy ETL pipeline:**

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Chạy ETL pipeline
python scripts/run_etl.py
```

### 4. Khám phá dữ liệu

#### **Chạy Jupyter Notebook:**

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Khởi động Jupyter
jupyter notebook notebooks/data_exploration.ipynb
```

### 5. Kết nối PowerBI

#### **Cấu hình PowerBI:**

1. Mở PowerBI Desktop
2. Chọn "Get Data" → "Database" → "PostgreSQL database"
3. Nhập thông tin kết nối:
    - Server: `localhost`
    - Database: `supermarket_sales`
    - Username: `supermarket_user`
    - Password: `supermarket_pass`
4. Chọn tables để import

## 📊 Kết quả mong đợi

### **Data Warehouse Tables:**

-   `dim_customer` (4 records)
-   `dim_product` (993 records)
-   `dim_time` (994 records)
-   `dim_branch` (3 records)
-   `dim_payment` (3 records)
-   `fact_sales` (1000 records)

### **PowerBI Dashboard có thể tạo:**

-   📈 Sales Overview Dashboard
-   🏪 Branch Performance Analysis
-   👥 Customer Segmentation
-   📦 Product Line Analysis
-   💳 Payment Method Trends
-   ⭐ Customer Rating Analysis

## 🔧 Troubleshooting

### **Lỗi database connection:**

```bash
# Kiểm tra PostgreSQL service
sudo systemctl status postgresql

# Khởi động service
sudo systemctl start postgresql
```

### **Lỗi permissions:**

```bash
# Cấp quyền cho user
sudo -u postgres psql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO supermarket_user;
```

### **Test connection:**

```bash
# Test database connection
python -c "from src.database.connection import test_connection; test_connection()"
```

## 📈 Performance Tips

1. **Indexing**: Database đã có indexes cho performance
2. **Batch Processing**: ETL xử lý theo batch 1000 records
3. **Logging**: Tất cả operations được log
4. **Error Handling**: Retry mechanism cho failed operations

## 🎯 Next Steps

1. ✅ Setup PostgreSQL database
2. ✅ Cấu hình .env file
3. ✅ Chạy ETL pipeline
4. ✅ Tạo PowerBI dashboard
5. ✅ Document insights và findings

---

**🎉 Chúc mừng! Bạn đã có một Data Warehouse hoàn chỉnh cho Supermarket Sales!**
