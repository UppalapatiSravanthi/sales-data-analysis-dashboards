"""
====================================================================
Page 7: Project Documentation and Architectural Overview
====================================================================
"""

import os
import streamlit as st

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='page-title'>ℹ️ About the Project: Architectural & Academic Overview</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Comprehensive documentation on problem formulation, system design, data pipeline, and software specifications.</p>", unsafe_allow_html=True)

# --------------------------------------------------
# Documentation Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Abstract & Problem Statement",
    "🎯 Objectives & System Comparison",
    "🏗️ System Architecture & Modules",
    "⚙️ Tech Stack & Requirements",
    "🚀 Advantages & Future Scope"
])

# Tab 1: Abstract & Problem
with tab1:
    st.subheader("Project Title")
    st.markdown("**Sales Data Analysis and Visualization Dashboard Using Python**")

    st.subheader("Project Abstract")
    st.write("""
    In modern commerce, data-driven decision-making is essential for sustaining profitability and operational efficiency. 
    This project delivers a complete, modular, and beginner-friendly Data Science application developed entirely in Python. 
    It ingests sales transaction data from CSV and Excel spreadsheets, cleanses and validates records, persists transactions 
    into a local SQLite relational database, performs deterministic descriptive and exploratory analysis, and renders 
    rich interactive visualizations using Plotly, Matplotlib, and Streamlit.
    
    Crucially, the system avoids "black-box" Machine Learning, Deep Learning, or speculative AI predictive modeling. 
    Instead, it focuses strictly on transparent, reliable, and auditable statistical aggregation, profit and loss breakdown, 
    and authentic business insight synthesis based on factual mathematical calculations.
    """)

    st.subheader("Problem Statement")
    st.write("""
    Traditional small-to-medium businesses frequently maintain sales data across disparate, unorganized CSV files or static 
    spreadsheets. Common challenges include:
    1. **Data Inconsistency:** Duplicate invoice records, missing quantity/price values, and mismatched dates.
    2. **Lack of Instant Visibility:** Calculating monthly growth, regional profitability, or product rankings manually in spreadsheets is cumbersome, slow, and prone to human arithmetic errors.
    3. **Disconnected Databases:** File-based records lack relational constraints, leading to data loss or duplicate entries.
    4. **Over-Engineered AI Tools:** Modern analytics tools often introduce unnecessary, complex predictive machine learning models that are difficult for business stakeholders to interpret, audit, or trust.
    """)

# Tab 2: Objectives & Comparison
with tab2:
    st.subheader("Project Objectives")
    st.markdown("""
    - **Automated Data Cleaning:** Provide an intuitive interface to detect missing values, purge duplicate rows, and recalculate financial metrics ($Total\\ Sales = Quantity \\times Unit\\ Price$, $Profit = Total\\ Sales - Cost$).
    - **Relational Persistence:** Store and retrieve transactions seamlessly with an embedded SQLite database (`sales.db`) enforcing unique Order IDs.
    - **Interactive Visual Cockpit:** Provide interactive Plotly charts (bar, line, pie, donut, histogram, scatter, and heatmaps) with instant multi-filter reactivity.
    - **In-Depth Business Analysis:** Segment data across temporal (monthly/yearly), categorical, geographic, and customer dimensions.
    - **Certified Report Generation:** Provide one-click downloads for filtered datasets (CSV), comprehensive multi-tab Excel workbooks (`.xlsx`), and markdown executive briefs.
    """)

    st.subheader("Existing System vs. Proposed System")
    st.markdown("""
    | Parameter | Existing System (Static Spreadsheets) | Proposed System (Streamlit Python Dashboard) |
    |---|---|---|
    | **Data Storage** | Disconnected local files (.csv/.xlsx) | Centralized SQLite database with uniqueness validation |
    | **Data Cleaning** | Manual row-by-row inspection | Automated diagnostics, imputation, and duplicate removal |
    | **Interactivity** | Static charts requiring manual rebuilds | Dynamic Plotly charts reactive to sidebar filters |
    | **Insights** | Requires manual pivot tables and formulas | Computed deterministically with automated executive narratives |
    | **Reporting** | Time-consuming manual formatting | One-click multi-sheet Excel, CSV, and Markdown exports |
    | **Interpretability**| High variance in human spreadsheet formulas | 100% auditable, deterministic open-source Python logic |
    """)

# Tab 3: Modules & Architecture
with tab3:
    st.subheader("System Modules")
    st.markdown("""
    1. **Data Generation Module (`generate_dataset.py`):**
       Generates realistic multi-year synthetic transactions across 25 products, 4 categories, and 5 regions.
    2. **Database Module (`database.py`):**
       Manages SQLite table schema, index creation, unique transaction checks, and bulk ingestion.
    3. **Data Cleaning Module (`data_cleaning.py`):**
       Standardizes naming conventions, handles null values via statistical imputation or truncation, and validates mathematical invariants.
    4. **Analysis & Statistical Engine (`data_analysis.py`):**
       Computes high-level KPIs, Month-over-Month (MoM) growth rates, Year-over-Year (YoY) metrics, product rankings, and descriptive spread statistics.
    5. **Visualization Engine (`visualization.py`):**
       Implements responsive Plotly figures and Matplotlib multi-panel layouts.
    6. **Report Generation Module (`report_generation.py`):**
       Builds multi-tab Excel workbooks via `openpyxl`, formats CSV bytes, and generates markdown narrative summaries.
    7. **Interactive User Interface (`app.py` & `pages/`):**
       Modular multi-page Streamlit web application styled with modern CSS cards.
    """)

# Tab 4: Tech Stack & Requirements
with tab4:
    col_tech1, col_tech2 = st.columns(2)

    with col_tech1:
        st.subheader("Software Requirements")
        st.markdown("""
        - **Operating System:** Windows 10/11, macOS, or Linux
        - **Programming Language:** Python 3.9+ (tested up to Python 3.14)
        - **Web Framework:** Streamlit
        - **Data Processing:** Pandas, NumPy
        - **Visualization:** Plotly, Matplotlib, Seaborn
        - **Database:** SQLite3 (standard library)
        - **Spreadsheet Engines:** openpyxl, xlsxwriter
        - **IDE:** Visual Studio Code / PyCharm
        """)

    with col_tech2:
        st.subheader("Hardware Requirements")
        st.markdown("""
        - **Processor:** Intel Core i3 / AMD Ryzen 3 or higher
        - **RAM:** Minimum 4 GB (8 GB recommended for large datasets)
        - **Storage:** 500 MB free disk space
        - **Display:** 1366x768 resolution minimum (1080p recommended)
        - **Network:** Only required during initial package installation via pip
        """)

# Tab 5: Advantages & Future Scope
with tab5:
    st.subheader("Key Advantages")
    st.markdown("""
    - **Zero Black-Box Guesswork:** Completely avoids unpredictable AI hallucination or statistical drift.
    - **Complete Transparency:** Every KPI and insight is verifiable through basic arithmetic.
    - **Lightweight & Fast:** Runs locally with zero external API fees or server dependencies.
    - **Beginner-Friendly Architecture:** Clean, modular code structure following PEP-8 standards.
    """)

    st.subheader("Future Enhancements")
    st.markdown("""
    - **Multi-User Role Authentication:** Add role-based access control (Admin, Manager, Analyst).
    - **Direct Cloud Database Integration:** Connect to PostgreSQL, MySQL, or Snowflake.
    - **Scheduled Email Reports:** Automated weekly PDF delivery using SMTP or webhooks.
    - **Currency & Multi-Tax Support:** Handle multi-currency transactions and VAT/sales tax calculations.
    - **Inventory Threshold Alerts:** Highlight stock replenishment triggers when unit quantities cross minimum thresholds.
    """)

    st.subheader("Conclusion")
    st.write("""
    The Sales Data Analysis and Visualization Dashboard demonstrates the power of clean software engineering and 
    rigorous statistical exploratory analysis in Python. By uniting pandas, SQLite, Plotly, and Streamlit into a cohesive 
    multi-page application, it empowers decision-makers with instantaneous, trustworthy operational visibility.
    """)
