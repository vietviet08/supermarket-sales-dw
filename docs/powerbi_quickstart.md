# PowerBI Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Import Data (2 minutes)

1. Open PowerBI Desktop
2. **Get Data** → **Text/CSV**
3. Import these files from `data/warehouse/`:
    - ✅ `sales_summary.csv` (Main dataset)
    - ✅ `sales_by_branch.csv` (Geographic data)
    - ✅ `sales_by_product.csv` (Product data)

### Step 2: Create Basic Dashboard (3 minutes)

#### **KPI Cards**:

-   **Total Sales**: `SUM(sales_summary[sales])`
-   **Total Transactions**: `COUNTROWS(sales_summary)`
-   **Average Order Value**: `AVERAGE(sales_summary[sales])`
-   **Customer Rating**: `AVERAGE(sales_summary[rating])`

#### **Key Charts**:

1. **Sales by Branch** (Bar Chart)

    - X: `branch`
    - Y: `sales`

2. **Top Products** (Horizontal Bar Chart)

    - X: `product_line`
    - Y: `sales`

3. **Monthly Trend** (Line Chart)

    - X: `month`
    - Y: `sales`

4. **Customer Analysis** (Pie Chart)
    - Legend: `customer_type`
    - Values: `sales`

## 📊 Sample Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│  Total Sales    │  Transactions  │  AOV    │  Rating    │
│  $322,969       │  1,000         │  $323   │  7.0/10    │
└─────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Sales by       │  │  Top Products   │  │  Monthly Trend  │
│  Branch         │  │                 │  │                 │
│  [Bar Chart]    │  │  [Bar Chart]    │  │  [Line Chart]   │
└─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Customer Analysis                                     │
│  [Pie Chart: Member vs Normal]                        │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Quick Formatting

### **Colors**:

-   Primary: Blue (#1f77b4)
-   Secondary: Orange (#ff7f0e)
-   Success: Green (#2ca02c)

### **Fonts**:

-   Headers: Segoe UI Bold, 16pt
-   Values: Segoe UI, 14pt
-   Labels: Segoe UI, 12pt

## 🔧 Advanced Features (Optional)

### **Filters**:

-   Add slicers for: Branch, Product Line, Date Range
-   Position at top of dashboard

### **Drill-through**:

-   Click on branch → see detailed transactions
-   Click on product → see sales over time

### **Mobile Layout**:

-   Optimize for mobile devices
-   Stack charts vertically
-   Use larger touch targets

## 📈 Ready-to-Use DAX Measures

Copy and paste these into PowerBI:

```DAX
Total Sales = SUM(sales_summary[sales])
Total Transactions = COUNTROWS(sales_summary)
Average Order Value = AVERAGE(sales_summary[sales])
Customer Rating = AVERAGE(sales_summary[rating])
Sales Growth =
VAR CurrentMonth = MAX(sales_summary[month])
VAR PreviousMonth = CurrentMonth - 1
VAR CurrentSales = CALCULATE([Total Sales], sales_summary[month] = CurrentMonth)
VAR PreviousSales = CALCULATE([Total Sales], sales_summary[month] = PreviousMonth)
RETURN
IF(PreviousSales > 0, (CurrentSales - PreviousSales) / PreviousSales, 0)
```

## 🚀 Publish to PowerBI Service

1. **File** → **Publish** → **Publish to PowerBI**
2. Select workspace
3. **Set up automatic refresh** (if needed)
4. **Share** with stakeholders

## 📱 Mobile Optimization

-   Use **Phone Layout** in PowerBI Desktop
-   Stack charts vertically
-   Use larger fonts
-   Simplify interactions

---

**That's it! Your dashboard is ready in 5 minutes! 🎉**
