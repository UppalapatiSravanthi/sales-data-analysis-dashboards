# Sales Data Analysis and Visualization Dashboard Using Python

A complete, professional, beginner-friendly Data Science application developed strictly using Python, Pandas, SQLite, Plotly, and Streamlit. This project performs exploratory data analysis, data cleaning, relational data persistence, statistical calculation, interactive charting, and executive report generation.

> **CRITICAL DESIGN PRINCIPLE:** This project explicitly avoids Machine Learning, Deep Learning, and AI prediction models. It focuses 100% on auditable, reliable, deterministic Data Analysis, Data Cleaning, Statistical Summaries, and Interactive Visualizations.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Complete Project Folder Structure](#complete-project-folder-structure)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [Installation & Setup Guide](#installation--setup-guide)
6. [Running the Application](#running-the-application)
7. [Step-by-Step Testing & Verification](#step-by-step-testing--verification)
8. [Database Architecture & Schema](#database-architecture--schema)
9. [Academic & Project Report Documentation](#academic--project-report-documentation)
   - Abstract
   - Problem Statement
   - Objectives
   - Existing vs. Proposed System
   - System Modules
   - Software & Hardware Requirements
   - Advantages
   - Future Enhancements
   - Conclusion

---

## 1. Project Overview

The **Sales Data Analysis and Visualization Dashboard** is an enterprise-grade business intelligence tool designed for commercial organizations to track sales performance, evaluate profit margins, discover regional trends, identify top-selling products, and export executive reports with ease.

---

## 2. Complete Project Folder Structure

```text
sales_data_analysis/
│
├── app.py                      # Main entry point & Executive Overview
├── requirements.txt            # Python package dependencies
├── README.md                   # Complete documentation & user manual
├── database.py                 # SQLite database connection & CRUD operations
├── data_cleaning.py            # Data diagnostics, cleaning & validation pipeline
├── data_analysis.py            # Descriptive statistics, KPIs & analytical aggregations
├── visualization.py            # Plotly interactive charts & Matplotlib reports
├── report_generation.py        # Multi-tab Excel, CSV & Markdown report exporter
├── generate_dataset.py         # Synthetic multi-year sales dataset generator
├── sales.db                    # Embedded SQLite relational database (auto-generated)
│
├── datasets/
│   └── sales_data.csv          # Sample sales dataset (1,250 realistic records)
│
├── pages/
│   ├── 1_Dashboard.py          # Executive multi-metric interactive dashboard
│   ├── 2_Data_Upload.py        # CSV & Excel ingestion with schema diagnostics
│   ├── 3_Data_Cleaning.py      # Missing value imputation & anomaly remediation studio
│   ├── 4_Sales_Analysis.py     # Deep temporal, product, category & customer analytics
│   ├── 5_Visualization.py      # Interactive chart catalog (Bar, Line, Pie, Scatter, Heatmap)
│   ├── 6_Reports.py            # Multi-sheet Excel workbook & Markdown report downloads
│   └── 7_About.py              # Architecture, system specifications & documentation
│
└── assets/
    └── style.css               # Modern CSS theme & KPI metric card styling
```

---

## 3. Key Features

### A. Executive Dashboard
- **Total Sales Revenue:** Real-time summation of gross sales.
- **Total Profit:** Net profit calculated after deducting product cost.
- **Total Orders:** Count of unique invoices processed.
- **Total Products Sold:** Aggregate volume of units dispatched.
- **Average Order Value (AOV):** Mean dollar spend per transaction.
- **Profit Margin (%):** Operational profitability ratio.

### B. Ingestion & File Upload
- Upload external `.csv`, `.xlsx`, or `.xls` spreadsheets.
- Instant schema diagnostics: row count, column count, data types, null cell count, and duplicate count.
- Direct synchronization with SQLite with unique `Order ID` constraints to prevent duplicates.

### C. Data Cleaning Studio
- Automated column name standardization (casing, underscores, spacing).
- Missing value remediation (statistical median/mode imputation or record deletion).
- Duplicate transaction removal.
- Mathematical integrity recalculation ($Total\ Sales = Quantity \times Unit\ Price$, $Profit = Total\ Sales - Cost$).
- Side-by-side comparison (Before vs. After Cleaning).
- Instant export of cleaned data.

### D. Advanced Statistical Analysis
- **Monthly & Yearly Trends:** Month-over-Month (MoM) and Year-over-Year (YoY) percentage growth rates.
- **Product Rankings:** Top 10 best-selling items, top 10 highest-profit drivers, and lowest-performing items.
- **Categorical & Regional Breakdowns:** Revenue share percentage and margin efficiency.
- **Customer Analytics:** Top 15 highest-spending clients and order frequencies.
- **Profit & Loss Analysis:** Profitable vs. clearance/loss transactions.
- **Descriptive Statistics:** Full mathematical distribution tables (Mean, Median, Standard Deviation, Variance, Min, Max, Quartiles).
- **Computed Business Insights:** 8 factual, math-backed business insights derived directly from data.

### E. Interactive Visualizations (Plotly & Matplotlib)
- **Bar Chart:** Top N best-selling products.
- **Line Chart:** Monthly sales and profit trends with markers.
- **Pie Chart:** Category revenue share.
- **Donut Chart:** Geographic sales split.
- **Histogram:** Transaction value distribution.
- **Scatter Plot:** Sales vs. Profit correlation colored by category with break-even marker.
- **Heatmap:** Category sales volume across operating months.
- **Matplotlib Multi-Panel Figure:** 2x2 static grid for print and formal publications.

### F. Multi-Format Report Center
- **Multi-Sheet Excel Workbook (`.xlsx`):** Multi-tab executive report including Summary, Raw Filtered Rows, Monthly Breakdown, Category Analysis, Regional Breakdown, and Top Products.
- **Filtered CSV Export:** Clean export of active filtered view.
- **Executive Markdown Brief:** Downloadable narrative summary with timestamps and tables.

---

## 4. Technology Stack

- **Python (3.9+)**
- **Pandas:** Tabular data transformation, cleaning, grouping, and aggregations.
- **NumPy:** Mathematical calculations and array operations.
- **Streamlit:** Modern multi-page web application interface.
- **Plotly:** Interactive web-based data visualizations.
- **Matplotlib & Seaborn:** Publication-quality static charting.
- **SQLite3:** Embedded relational storage and ACID-compliant persistence.
- **OpenPyXL & XlsxWriter:** Multi-tab Excel spreadsheet generation.

---

## 5. Installation & Setup Guide

### Step 1: Install Python
Ensure Python 3.9 or higher is installed on your computer.
- Download from [python.org](https://www.python.org/downloads/)
- During installation on Windows, **check the box "Add python.exe to PATH"**.

### Step 2: Set Up Project Directory in VS Code
1. Open Visual Studio Code.
2. Select **File > Open Folder...** and choose the `sales_data_analysis` folder:
   ```text
   C:\Users\trive\.gemini\antigravity\scratch\sales_data_analysis
   ```
3. Open a new terminal in VS Code (`Ctrl + ~` or **Terminal > New Terminal**).

### Step 3: Create and Activate Virtual Environment
In your terminal, run:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Required Libraries
Install all required dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 6. Running the Application

### Step 1: Generate the Sample Dataset & Initialize SQLite Database
Run the dataset generator script to create `datasets/sales_data.csv` (1,250 realistic transactions) and initialize the SQLite database `sales.db`:
```bash
python generate_dataset.py
```

### Step 2: Launch the Streamlit Web Application
Execute the following command:
```bash
streamlit run app.py
```

The application will launch automatically in your default web browser at:
```text
http://localhost:8501
```

---

## 7. Step-by-Step Testing & Verification

1. **Dashboard Home (`app.py` & `pages/1_Dashboard.py`):**
   - Check that all 6 KPI cards populate with real numbers.
   - Adjust the **Date Range** slider or **Category** filter in the sidebar; observe that KPI cards and Plotly charts update in real time.
2. **Data Upload (`pages/2_Data_Upload.py`):**
   - Upload `datasets/sales_data.csv` or any custom Excel file.
   - Verify that row count, column count, and schema data types appear accurately.
   - Click **Save Records to SQLite** and observe the confirmation message.
3. **Data Cleaning (`pages/3_Data_Cleaning.py`):**
   - Review pre-cleaning diagnostics (missing values and duplicate rows).
   - Select the **Impute** strategy and check **Validate & Recompute Formulas**.
   - Compare the **Before vs. After** tabs.
   - Click **Download Cleaned CSV** to test file generation.
4. **Sales Analysis (`pages/4_Sales_Analysis.py`):**
   - Switch between tabs: Monthly Trends, Product Rankings, Categories, Customers, Profit & Loss, and Descriptive Statistics.
   - Check MoM and YoY percentage growth figures.
5. **Visualizations (`pages/5_Visualization.py`):**
   - Interact with the Bar Chart, Line Chart, Pie Chart, Donut Chart, Histogram, Scatter Plot, and Heatmap.
   - Check the static 2x2 Matplotlib composite view.
6. **Reports (`pages/6_Reports.py`):**
   - Click **Download Excel Workbook (.xlsx)** and open it in Microsoft Excel or Google Sheets. Verify all 6 sheets exist with formatted data.
   - Click **Download Markdown Report (.md)** and verify the narrative summary.

---

## 8. Database Architecture & Schema

The application uses an embedded SQLite database (`sales.db`) with an optimized `sales` table:

```sql
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL UNIQUE,
    order_date TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    region TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_sales REAL NOT NULL,
    cost REAL NOT NULL,
    profit REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date);
CREATE INDEX IF NOT EXISTS idx_category ON sales(category);
CREATE INDEX IF NOT EXISTS idx_region ON sales(region);
```

- **Duplicate Prevention:** The `UNIQUE` constraint on `order_id` along with `INSERT OR IGNORE` logic guarantees that uploading the same dataset multiple times will never duplicate sales numbers.
- **Relational Integrity:** Indexes on `order_date`, `category`, and `region` ensure sub-second query execution even across thousands of records.

---

## 9. Academic & Project Report Documentation

### Project Title
**Sales Data Analysis and Visualization Dashboard Using Python**

### Abstract
In contemporary retail and enterprise commerce, data-driven decision-making is essential for sustaining profitability and operational efficiency. This project delivers a complete, modular, and beginner-friendly Data Science application developed entirely in Python. It ingests sales transaction data from CSV and Excel spreadsheets, cleanses and validates records, persists transactions into a local SQLite relational database, performs deterministic descriptive and exploratory analysis, and renders rich interactive visualizations using Plotly, Matplotlib, and Streamlit.

Crucially, the system avoids "black-box" Machine Learning, Deep Learning, or speculative AI predictive modeling. Instead, it focuses strictly on transparent, reliable, and auditable statistical aggregation, profit and loss breakdown, and authentic business insight synthesis based on factual mathematical calculations.

### Problem Statement
Traditional businesses frequently maintain sales data across disparate, unorganized CSV files or static spreadsheets. Common challenges include:
1. **Data Inconsistency:** Duplicate invoice records, missing quantity/price values, and mismatched dates.
2. **Lack of Instant Visibility:** Calculating monthly growth, regional profitability, or product rankings manually in spreadsheets is cumbersome, slow, and prone to human arithmetic errors.
3. **Disconnected Databases:** File-based records lack relational constraints, leading to data loss or duplicate entries.
4. **Over-Engineered AI Tools:** Modern analytics tools often introduce unnecessary, complex predictive machine learning models that are difficult for business stakeholders to interpret, audit, or trust.

### Objectives
- Provide an automated cleaning pipeline to eliminate duplicates, impute missing values, and validate business formulas.
- Store records in an embedded relational SQLite database with duplicate-prevention constraints.
- Build an interactive, multi-filtered web dashboard with zero-latency updates.
- Calculate essential business KPIs: Gross Sales, Net Profit, Profit Margin, Total Orders, Units Sold, and Average Order Value.
- Generate certified, multi-tab Excel workbooks, CSV files, and Markdown executive summaries.

### Existing System vs. Proposed System

| Parameter | Existing System (Static Spreadsheets) | Proposed System (Streamlit Python Dashboard) |
|---|---|---|
| **Data Storage** | Disconnected local files (.csv/.xlsx) | Centralized SQLite database with uniqueness validation |
| **Data Cleaning** | Manual row-by-row inspection | Automated diagnostics, imputation, and duplicate removal |
| **Interactivity** | Static charts requiring manual rebuilds | Dynamic Plotly charts reactive to sidebar filters |
| **Insights** | Requires manual pivot tables and formulas | Computed deterministically with automated executive narratives |
| **Reporting** | Time-consuming manual formatting | One-click multi-sheet Excel, CSV, and Markdown exports |
| **Interpretability**| High variance in human spreadsheet formulas | 100% auditable, deterministic open-source Python logic |

### System Modules
1. **Data Generation Module (`generate_dataset.py`):** Generates realistic multi-year synthetic transactions across 25 products, 4 categories, and 5 regions.
2. **Database Module (`database.py`):** Manages SQLite table schema, index creation, unique transaction checks, and bulk ingestion.
3. **Data Cleaning Module (`data_cleaning.py`):** Standardizes naming conventions, handles null values via statistical imputation or truncation, and validates mathematical invariants.
4. **Analysis & Statistical Engine (`data_analysis.py`):** Computes high-level KPIs, Month-over-Month (MoM) growth rates, Year-over-Year (YoY) metrics, product rankings, and descriptive spread statistics.
5. **Visualization Engine (`visualization.py`):** Implements responsive Plotly figures and Matplotlib multi-panel layouts.
6. **Report Generation Module (`report_generation.py`):** Builds multi-tab Excel workbooks via `openpyxl`, formats CSV bytes, and generates markdown narrative summaries.
7. **Interactive User Interface (`app.py` & `pages/`):** Modular multi-page Streamlit web application styled with modern CSS cards.

### Software & Hardware Requirements

**Software Requirements:**
- Operating System: Windows 10/11, macOS, Linux
- Python 3.9+ (tested on Python 3.14)
- Packages: `streamlit`, `pandas`, `numpy`, `matplotlib`, `plotly`, `openpyxl`, `xlsxwriter`, `seaborn`
- Web Browser: Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari

**Hardware Requirements:**
- Processor: Intel Core i3 / AMD Ryzen 3 or higher
- RAM: 4 GB minimum (8 GB recommended)
- Disk Space: 500 MB free space

### Advantages
- **100% Verifiable & Explainable:** Every number and chart is calculated through direct arithmetic; no black-box predictions.
- **Relational Integrity:** Automatic SQLite schema guarantees that duplicates are rejected.
- **Zero Cost:** Built purely on free, open-source technologies with no subscription requirements.
- **High Portability:** Runs locally on any standard laptop or workstation.

### Future Enhancements
- **Multi-Role Authentication:** User authentication for Admin, Store Manager, and Sales Analyst roles.
- **Cloud Database Support:** Connectors for PostgreSQL, MySQL, and Snowflake.
- **Automated Email Reports:** Scheduled weekly executive PDF/Excel dispatch via SMTP.
- **Multi-Currency Support:** Automatic currency conversion based on historical exchange rates.

### Conclusion
The **Sales Data Analysis and Visualization Dashboard** demonstrates how standard Python libraries and exploratory data science techniques can be harmonized to build a production-quality analytics application. By prioritizing transparent calculations, clean data modeling, and intuitive design, the project provides business stakeholders with immediate, reliable insights without relying on complex, uninterpretable machine learning models.
