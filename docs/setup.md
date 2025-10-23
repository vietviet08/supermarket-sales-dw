# Hướng dẫn Setup dự án Supermarket Sales Data Warehouse

## 📋 Yêu cầu hệ thống

-   Python 3.8+
-   PostgreSQL 12+
-   Git
-   PowerBI Desktop (cho dashboard)

## 🔧 Cài đặt từng bước

### 1. Clone repository

```bash
git clone <repository-url>
cd supermarket-sales
```

### 2. Tạo virtual environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cài đặt PostgreSQL

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Windows:

-   Tải PostgreSQL từ https://www.postgresql.org/download/windows/
-   Cài đặt với default settings

#### macOS:

```bash
brew install postgresql
```

### 5. Setup Database

```bash
# Đăng nhập PostgreSQL
sudo -u postgres psql

# Tạo database
CREATE DATABASE supermarket_sales;

# Tạo user
CREATE USER supermarket_user WITH PASSWORD 'your_password';

# Cấp quyền
GRANT ALL PRIVILEGES ON DATABASE supermarket_sales TO supermarket_user;
```

### 6. Cấu hình environment

```bash
# Copy file template
cp env.example .env

# Chỉnh sửa file .env với thông tin database
nano .env
```

### 7. Tạo thư mục logs

```bash
mkdir -p logs
```

### 8. Test kết nối database

```bash
python -c "from src.database.connection import test_connection; test_connection()"
```

## 🚀 Chạy dự án

### 1. Tải dữ liệu từ Kaggle

```bash
# Tải file CSV từ Kaggle và đặt vào data/raw/
# File: supermarket_sales.csv
```

### 2. Chạy ETL process

```bash
# Extract
python src/etl/extract.py

# Transform
python src/etl/transform.py

# Load
python src/etl/load.py
```

### 3. Kiểm tra dữ liệu

```bash
# Chạy Jupyter notebook để kiểm tra
jupyter notebook notebooks/data_exploration.ipynb
```

## 🔍 Troubleshooting

### Lỗi kết nối database

-   Kiểm tra PostgreSQL service đang chạy
-   Kiểm tra thông tin trong file .env
-   Kiểm tra firewall settings

### Lỗi import modules

-   Đảm bảo virtual environment được kích hoạt
-   Chạy `pip install -r requirements.txt` lại

### Lỗi permissions

-   Kiểm tra quyền ghi file trong thư mục logs/
-   Kiểm tra quyền database user
