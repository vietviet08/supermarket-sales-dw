# PowerBI Dashboard Guide - Supermarket Sales Data Warehouse

## 📊 Overview

Hướng dẫn chi tiết để tạo PowerBI dashboard từ dữ liệu Supermarket Sales Data Warehouse đã được export.

## 🗂️ Data Sources Available

### 1. **Main Dataset** - `data/warehouse/sales_summary.csv`

-   **Mô tả**: Dataset chính chứa tất cả thông tin sales với denormalized view
-   **Records**: 1,000 transactions
-   **Columns**:
    -   `invoice_id`, `customer_type`, `gender`, `product_line`, `unit_price`
    -   `date`, `time`, `year`, `month`, `quarter`
    -   `branch`, `city`, `payment_method`
    -   `quantity`, `tax_5_percent`, `sales`, `cogs`, `gross_margin_percentage`, `gross_income`, `rating`

### 2. **Pre-aggregated Datasets** - Ready for PowerBI

#### **Geographic Analysis** - `sales_by_branch.csv`

```csv
branch,city,total_sales,transaction_count,avg_sales
A,Yangon,110568.75,340,325.20
C,Mandalay,106200.37,340,312.35
B,Naypyitaw,106200.37,320,331.88
```

#### **Product Performance** - `sales_by_product.csv`

```csv
product_line,total_sales,transaction_count,avg_unit_price
Health and beauty,49044.00,170,288.24
Electronic accessories,49193.00,170,289.37
Sports and travel,49044.00,170,288.24
Food and beverages,49044.00,170,288.24
Home and lifestyle,49044.00,170,288.24
Fashion accessories,49044.00,150,327.00
```

#### **Time Series Analysis** - `monthly_sales_trend.csv`

```csv
year,month,total_sales,transaction_count
2019,1,322969.49,1000
```

#### **Customer Analysis** - `customer_analysis.csv`

```csv
customer_type,gender,total_sales,transaction_count,avg_rating
Member,Female,161484.75,500,7.00
Normal,Female,161484.75,500,7.00
```

## 🚀 PowerBI Setup Guide

### Step 1: Import Data Sources

1. **Open PowerBI Desktop**
2. **Get Data** → **Text/CSV**
3. **Import các file sau**:
    ```
    data/warehouse/sales_summary.csv          (Main dataset)
    data/warehouse/sales_by_branch.csv        (Geographic analysis)
    data/warehouse/sales_by_product.csv       (Product performance)
    data/warehouse/monthly_sales_trend.csv    (Time series)
    data/warehouse/customer_analysis.csv      (Customer insights)
    ```

### Step 2: Data Modeling

#### **Create Relationships**:

-   **sales_summary** ↔ **sales_by_branch** (via branch, city)
-   **sales_summary** ↔ **sales_by_product** (via product_line)
-   **sales_summary** ↔ **monthly_sales_trend** (via year, month)
-   **sales_summary** ↔ **customer_analysis** (via customer_type, gender)

#### **Create Calculated Columns**:

```DAX
# Sales Growth Rate
Sales Growth =
VAR CurrentMonth = [month]
VAR PreviousMonth = CurrentMonth - 1
VAR CurrentSales = CALCULATE(SUM(sales_summary[sales]), sales_summary[month] = CurrentMonth)
VAR PreviousSales = CALCULATE(SUM(sales_summary[sales]), sales_summary[month] = PreviousMonth)
RETURN
IF(PreviousSales > 0, (CurrentSales - PreviousSales) / PreviousSales, 0)

# Customer Segment
Customer Segment =
IF(sales_summary[customer_type] = "Member", "Premium", "Standard")

# Product Category
Product Category =
SWITCH(
    sales_summary[product_line],
    "Health and beauty", "Personal Care",
    "Electronic accessories", "Electronics",
    "Sports and travel", "Sports",
    "Food and beverages", "Food",
    "Home and lifestyle", "Home",
    "Fashion accessories", "Fashion",
    "Other"
)
```

#### **Create Measures**:

```DAX
# Total Sales
Total Sales = SUM(sales_summary[sales])

# Average Order Value
AOV = AVERAGE(sales_summary[sales])

# Total Transactions
Total Transactions = COUNTROWS(sales_summary)

# Sales by Branch
Branch Sales =
SUMX(
    sales_by_branch,
    sales_by_branch[total_sales]
)

# Top Product
Top Product =
TOPN(1, sales_by_product, sales_by_product[total_sales], DESC)

# Customer Satisfaction
Avg Rating = AVERAGE(sales_summary[rating])

# Monthly Growth
Monthly Growth =
VAR CurrentMonth = MAX(sales_summary[month])
VAR PreviousMonth = CurrentMonth - 1
VAR CurrentSales = CALCULATE([Total Sales], sales_summary[month] = CurrentMonth)
VAR PreviousSales = CALCULATE([Total Sales], sales_summary[month] = PreviousMonth)
RETURN
IF(PreviousSales > 0, (CurrentSales - PreviousSales) / PreviousSales, 0)
```

## 📈 Dashboard Design Recommendations

### **Page 1: Executive Summary**

-   **KPI Cards**:

    -   Total Sales (with trend indicator)
    -   Total Transactions
    -   Average Order Value
    -   Customer Satisfaction Rating

-   **Charts**:
    -   Sales by Month (Line Chart)
    -   Sales by Branch (Bar Chart)
    -   Top 5 Products (Horizontal Bar Chart)

### **Page 2: Geographic Analysis**

-   **Map Visualization**:

    -   Sales by City (Bubble Map)
    -   Branch Performance (Table)
    -   Geographic Distribution (Pie Chart)

-   **Filters**:
    -   Branch
    -   City
    -   Date Range

### **Page 3: Product Performance**

-   **Product Analysis**:

    -   Sales by Product Line (Donut Chart)
    -   Product Performance Matrix (Scatter Plot)
    -   Unit Price vs Sales (Scatter Plot)

-   **Drill-down**:
    -   Product Line → Individual Products
    -   Time Period Analysis

### **Page 4: Customer Insights**

-   **Customer Analysis**:

    -   Sales by Customer Type (Stacked Bar)
    -   Gender Distribution (Pie Chart)
    -   Customer Rating Analysis (Histogram)

-   **Segmentation**:
    -   Member vs Normal customers
    -   High-value customers identification

### **Page 5: Time Series Analysis**

-   **Trend Analysis**:

    -   Monthly Sales Trend (Line Chart)
    -   Seasonal Patterns (Area Chart)
    -   Growth Rate Analysis (Waterfall Chart)

-   **Forecasting**:
    -   Sales Forecast (Line Chart with Prediction)
    -   Trend Analysis

## 🎨 Visual Design Best Practices

### **Color Scheme**:

-   **Primary**: #1f77b4 (Blue)
-   **Secondary**: #ff7f0e (Orange)
-   **Success**: #2ca02c (Green)
-   **Warning**: #d62728 (Red)
-   **Neutral**: #7f7f7f (Gray)

### **Chart Types**:

-   **KPI Cards**: Large numbers with trend indicators
-   **Time Series**: Line charts with smooth curves
-   **Comparisons**: Bar charts (horizontal for long labels)
-   **Distributions**: Pie charts for < 6 categories
-   **Correlations**: Scatter plots with trend lines

### **Layout Guidelines**:

-   **Grid System**: 12-column grid
-   **Spacing**: Consistent margins (16px, 24px, 32px)
-   **Typography**: Clear hierarchy (H1, H2, H3)
-   **Interactive Elements**: Hover effects, drill-through

## 🔧 Advanced Features

### **Drill-through Pages**:

1. **Product Detail Page**: Drill from product line to individual products
2. **Branch Detail Page**: Drill from branch to individual transactions
3. **Customer Detail Page**: Drill from customer segment to individual customers

### **Bookmarks and Buttons**:

-   **Navigation**: Between pages
-   **Filters**: Reset all filters
-   **Views**: Switch between different analysis views

### **Mobile Layout**:

-   **Responsive Design**: Optimize for mobile devices
-   **Touch-friendly**: Large buttons and touch targets
-   **Simplified Views**: Focus on key metrics

## 📊 Sample Queries for Advanced Analysis

### **DAX Queries**:

```DAX
# Top 10 Customers by Sales
Top Customers =
TOPN(10,
    SUMMARIZE(sales_summary, sales_summary[customer_type], sales_summary[gender]),
    [Total Sales],
    DESC
)

# Sales Growth by Product
Product Growth =
ADDCOLUMNS(
    sales_by_product,
    "Growth Rate",
    DIVIDE(
        [total_sales] - CALCULATE([total_sales], PREVIOUSMONTH(sales_summary[date])),
        CALCULATE([total_sales], PREVIOUSMONTH(sales_summary[date]))
    )
)

# Customer Lifetime Value
CLV =
SUMX(
    SUMMARIZE(sales_summary, sales_summary[customer_type]),
    [Total Sales] * [Total Transactions]
)
```

## 🚀 Deployment Guide

### **PowerBI Service**:

1. **Publish to PowerBI Service**
2. **Create Workspace**: "Supermarket Sales Analytics"
3. **Set up Data Gateway**: For automatic refresh
4. **Configure Refresh Schedule**: Daily at 6 AM

### **Sharing and Security**:

-   **Workspace Access**: Grant access to stakeholders
-   **Row-level Security**: Implement if needed
-   **App Distribution**: Create app for end users

### **Performance Optimization**:

-   **Data Model**: Optimize relationships
-   **Measures**: Use efficient DAX
-   **Visuals**: Limit data points
-   **Refresh**: Schedule appropriately

## 📈 Success Metrics

### **Dashboard KPIs**:

-   **Load Time**: < 3 seconds
-   **User Engagement**: > 80% monthly active users
-   **Data Freshness**: < 24 hours
-   **Accuracy**: 100% data validation

### **Business Impact**:

-   **Decision Speed**: 50% faster insights
-   **Data Accessibility**: Self-service analytics
-   **Cost Reduction**: Reduced manual reporting
-   **Revenue Impact**: Data-driven decisions

---

## 🎯 Quick Start Checklist

-   [ ] Import all CSV files from `data/warehouse/`
-   [ ] Create relationships between tables
-   [ ] Build basic KPI cards
-   [ ] Add geographic analysis
-   [ ] Implement product performance views
-   [ ] Create customer insights
-   [ ] Add time series analysis
-   [ ] Apply consistent formatting
-   [ ] Test on mobile devices
-   [ ] Publish to PowerBI Service
-   [ ] Set up automatic refresh
-   [ ] Share with stakeholders

**Happy Dashboarding! 🚀**
