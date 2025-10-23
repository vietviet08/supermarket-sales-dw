# PowerBI Database Connection Guide

## 🗄️ Direct PostgreSQL Connection

### **Connection Details**:

```
Server: localhost
Port: 5432
Database: supermarket_sales
Username: root
Password: [from .env file]
```

## 🔌 PowerBI Setup

### **Step 1: Connect to PostgreSQL**

1. **Get Data** → **Database** → **PostgreSQL database**
2. **Server**: `localhost`
3. **Database**: `supermarket_sales`
4. **Username**: `root`
5. **Password**: [Enter password from .env file]

### **Step 2: Select Tables**

Import these tables:

-   ✅ `v_sales_summary` (Main view - 1,000 records)
-   ✅ `dim_customer` (Customer dimensions)
-   ✅ `dim_product` (Product dimensions)
-   ✅ `dim_time` (Time dimensions)
-   ✅ `dim_branch` (Branch dimensions)
-   ✅ `dim_payment` (Payment dimensions)
-   ✅ `fact_sales` (Fact table)

## 📊 Recommended Views

### **Primary View**: `v_sales_summary`

-   **Description**: Denormalized view with all sales data
-   **Records**: 1,000 transactions
-   **Use for**: Main dashboard, all analysis

### **Dimension Tables**: For filtering and relationships

-   **dim_customer**: Customer types and gender
-   **dim_product**: Product lines and prices
-   **dim_time**: Date/time hierarchies
-   **dim_branch**: Branch locations
-   **dim_payment**: Payment methods

## 🔄 Data Refresh Setup

### **Automatic Refresh**:

1. **Gateway Setup**: Install On-premises data gateway
2. **Refresh Schedule**: Daily at 6:00 AM
3. **Credentials**: Store database credentials securely

### **Manual Refresh**:

-   **Refresh Now**: In PowerBI Service
-   **Scheduled Refresh**: Set up in dataset settings

## 📈 Sample Queries

### **Custom SQL Queries** (Optional):

```sql
-- Top 10 Products by Sales
SELECT
    product_line,
    SUM(sales) as total_sales,
    COUNT(*) as transaction_count
FROM v_sales_summary
GROUP BY product_line
ORDER BY total_sales DESC
LIMIT 10;

-- Monthly Sales Trend
SELECT
    year,
    month,
    SUM(sales) as total_sales,
    COUNT(*) as transaction_count
FROM v_sales_summary
GROUP BY year, month
ORDER BY year, month;

-- Customer Analysis
SELECT
    customer_type,
    gender,
    SUM(sales) as total_sales,
    AVG(rating) as avg_rating
FROM v_sales_summary
GROUP BY customer_type, gender
ORDER BY total_sales DESC;
```

## 🔧 Performance Optimization

### **Data Model**:

-   **Relationships**: Auto-detect relationships
-   **Cardinality**: Many-to-one for dimensions
-   **Cross-filter**: Both directions

### **Measures**:

```DAX
# Total Sales
Total Sales = SUM(v_sales_summary[sales])

# Average Order Value
AOV = AVERAGE(v_sales_summary[sales])

# Sales by Branch
Branch Sales =
SUMX(
    dim_branch,
    CALCULATE([Total Sales])
)

# Top Product
Top Product =
TOPN(1,
    dim_product,
    [Total Sales],
    DESC
)
```

## 🚀 Deployment Options

### **Option 1: Direct Database Connection**

-   **Pros**: Real-time data, no file management
-   **Cons**: Requires database access, gateway setup
-   **Best for**: Production environments

### **Option 2: CSV Export (Current)**

-   **Pros**: Simple setup, no database access needed
-   **Cons**: Manual refresh, file management
-   **Best for**: Development, demos

### **Option 3: Hybrid Approach**

-   **Development**: Use CSV files
-   **Production**: Use database connection
-   **Best for**: Full production deployment

## 🔒 Security Considerations

### **Database Security**:

-   **SSL Connection**: Enable SSL for production
-   **User Permissions**: Create read-only user for PowerBI
-   **Network Security**: Restrict database access

### **PowerBI Security**:

-   **Row-level Security**: Implement if needed
-   **Workspace Access**: Control user permissions
-   **Data Classification**: Mark sensitive data

## 📊 Sample Dashboard Queries

### **Executive Dashboard**:

```sql
-- KPI Summary
SELECT
    COUNT(*) as total_transactions,
    SUM(sales) as total_sales,
    AVG(sales) as avg_order_value,
    AVG(rating) as avg_rating
FROM v_sales_summary;
```

### **Geographic Analysis**:

```sql
-- Sales by Branch and City
SELECT
    branch,
    city,
    SUM(sales) as total_sales,
    COUNT(*) as transaction_count
FROM v_sales_summary
GROUP BY branch, city
ORDER BY total_sales DESC;
```

### **Product Performance**:

```sql
-- Top Products
SELECT
    product_line,
    SUM(sales) as total_sales,
    COUNT(*) as transaction_count,
    AVG(unit_price) as avg_unit_price
FROM v_sales_summary
GROUP BY product_line
ORDER BY total_sales DESC;
```

## 🎯 Quick Start Checklist

-   [ ] Install PostgreSQL connector in PowerBI
-   [ ] Test database connection
-   [ ] Import `v_sales_summary` view
-   [ ] Import dimension tables
-   [ ] Create relationships
-   [ ] Build basic KPI cards
-   [ ] Add geographic analysis
-   [ ] Implement product performance
-   [ ] Set up data refresh
-   [ ] Publish to PowerBI Service
-   [ ] Configure security settings
-   [ ] Share with stakeholders

---

**Ready to connect to your data warehouse! 🚀**
