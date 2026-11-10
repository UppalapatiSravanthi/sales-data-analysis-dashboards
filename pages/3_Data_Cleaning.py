"""
====================================================================
Page 3: Data Cleaning and Preprocessing Studio
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from database import get_active_dataset, save_to_database, clear_database
from data_cleaning import inspect_dataset, clean_sales_dataset
from report_generation import export_to_csv, export_to_excel

st.set_page_config(page_title="Data Cleaning Studio", page_icon="🧹", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='page-title'>🧹 Data Cleaning & Preprocessing Studio</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Detect data anomalies, remediate missing records, purge duplicates, and validate business formulas.</p>", unsafe_allow_html=True)

# Ensure base dataset is available
if "sales_data" not in st.session_state or st.session_state["sales_data"] is None or st.session_state["sales_data"].empty:
    st.session_state["sales_data"] = get_active_dataset()

df_to_clean = st.session_state["sales_data"]

if df_to_clean is None or df_to_clean.empty:
    st.warning("⚠️ No dataset currently loaded to clean. Please visit the Data Upload page first.")
else:
    # --------------------------------------------------
    # Initial Diagnostics
    # --------------------------------------------------
    raw_report = inspect_dataset(df_to_clean)

    st.subheader("1. Pre-Cleaning Diagnostics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", f"{raw_report['rows']:,}")
    c2.metric("Total Columns", f"{raw_report['columns']:,}")
    c3.metric("Missing Value Cells", f"{raw_report['total_missing']:,}")
    c4.metric("Duplicate Rows", f"{raw_report['duplicate_rows']:,}")

    # --------------------------------------------------
    # Cleaning Configurations
    # --------------------------------------------------
    st.subheader("2. Cleaning Rules & Strategy Selection")

    col_opt1, col_opt2, col_opt3 = st.columns(3)

    with col_opt1:
        missing_strat = st.selectbox(
            "Missing Value Strategy",
            options=["impute", "drop", "none"],
            format_func=lambda x: {
                "impute": "Impute (Median for numeric, Mode for text)",
                "drop": "Drop Rows with Any Missing Value",
                "none": "Keep Missing Values As-Is"
            }[x]
        )

    with col_opt2:
        drop_dups = st.checkbox(
            "Purge Duplicate Transactions",
            value=True,
            help="Removes rows where all columns or Order IDs are identical."
        )

    with col_opt3:
        recalc_formulas = st.checkbox(
            "Validate & Recompute Formulas",
            value=True,
            help="Enforces Total Sales = Quantity × Unit Price and Profit = Total Sales - Cost."
        )

    # Execute cleaning
    cleaned_df, clean_log = clean_sales_dataset(
        df_to_clean,
        handle_missing_strategy=missing_strat,
        drop_duplicates_flag=drop_dups,
        recalculate_metrics=recalc_formulas
    )

    cleaned_report = inspect_dataset(cleaned_df)

    # --------------------------------------------------
    # Cleaning Results Summary
    # --------------------------------------------------
    st.subheader("3. Cleaning Audit Log")
    
    l1, l2, l3, l4 = st.columns(4)
    l1.metric("Rows Prior", f"{clean_log['initial_rows']:,}")
    l2.metric("Duplicates Purged", f"{clean_log['duplicates_removed']:,}")
    l3.metric("Nulls Handled", f"{clean_log['missing_values_handled']:,}")
    l4.metric("Final Cleaned Rows", f"{clean_log['final_rows']:,}")

    # --------------------------------------------------
    # Before vs After Comparison
    # --------------------------------------------------
    st.subheader("4. Before vs After Comparison")
    comp_tab1, comp_tab2 = st.tabs(["✨ Cleaned Data View", "📋 Original Data View"])

    with comp_tab1:
        st.dataframe(cleaned_df.head(50), use_container_width=True)

    with comp_tab2:
        st.dataframe(df_to_clean.head(50), use_container_width=True)

    # --------------------------------------------------
    # Actions: Apply to Database or Download
    # --------------------------------------------------
    st.subheader("5. Apply or Export Cleaned Dataset")
    
    act_col1, act_col2, act_col3 = st.columns(3)

    with act_col1:
        if st.button("💾 Apply & Update SQLite Database", type="primary", use_container_width=True):
            clear_database()
            ins, skp = save_to_database(cleaned_df)
            st.session_state["sales_data"] = cleaned_df
            st.session_state["filtered_data"] = cleaned_df.copy()
            st.success(f"Database cleanly synchronized! {ins:,} validated records committed.")

    with act_col2:
        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=export_to_csv(cleaned_df),
            file_name="cleaned_sales_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with act_col3:
        st.download_button(
            label="⬇️ Download Cleaned Excel (.xlsx)",
            data=export_to_excel(cleaned_df),
            file_name="cleaned_sales_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
