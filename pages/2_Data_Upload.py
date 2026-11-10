"""
====================================================================
Page 2: Data Upload and Dataset Ingestion
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from database import save_to_database, load_from_database, get_table_summary, clear_database
from data_cleaning import inspect_dataset, standardize_columns
from report_generation import export_to_csv, export_to_excel

st.set_page_config(page_title="Data Upload", page_icon="📁", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='page-title'>📁 Sales Dataset Ingestion & Upload</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Upload external CSV or Excel spreadsheets, inspect schema properties, and synchronize with SQLite.</p>", unsafe_allow_html=True)

# --------------------------------------------------
# File Upload Interface
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Select a sales dataset file (CSV or Excel)",
    type=["csv", "xlsx", "xls"],
    help="Supports comma-separated files (.csv) and Microsoft Excel spreadsheets (.xlsx, .xls)."
)

df_uploaded = None

if uploaded_file is not None:
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        with st.spinner("Parsing uploaded file..."):
            if file_ext == "csv":
                df_uploaded = pd.read_csv(uploaded_file)
            else:
                df_uploaded = pd.read_excel(uploaded_file)

        df_uploaded = standardize_columns(df_uploaded)
        st.success(f"Successfully loaded file: **{uploaded_file.name}** ({len(df_uploaded):,} rows, {len(df_uploaded.columns)} columns)")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# --------------------------------------------------
# Display Diagnostics and Inspection
# --------------------------------------------------
if df_uploaded is not None and not df_uploaded.empty:
    report = inspect_dataset(df_uploaded)

    st.subheader("📋 Dataset Structure & Metrics")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rows", f"{report['rows']:,}")
    m2.metric("Total Columns", f"{report['columns']:,}")
    m3.metric("Total Missing Values", f"{report['total_missing']:,}")
    m4.metric("Duplicate Rows", f"{report['duplicate_rows']:,}")

    # Data Preview Tab & Types Tab
    tab1, tab2, tab3 = st.tabs(["📄 Data Preview", "🏷️ Column Types & Nulls", "💾 Database Sync"])

    with tab1:
        st.dataframe(df_uploaded.head(50), use_container_width=True)

    with tab2:
        schema_df = pd.DataFrame([
            {
                "Column Name": col,
                "Data Type": report["dtypes"].get(col, "Unknown"),
                "Missing Values": report["missing_values"].get(col, 0),
                "Missing (%)": f"{(report['missing_values'].get(col, 0) / report['rows'] * 100):.2f}%"
            }
            for col in report["column_names"]
        ])
        st.dataframe(schema_df, use_container_width=True)

    with tab3:
        st.markdown("### Persist Uploaded Records to SQLite Database")
        st.write("This operation merges uploaded records into the primary SQLite database (`sales.db`). Records with existing Order IDs will be safely skipped to guarantee uniqueness.")

        col_save, col_clear = st.columns([1, 1])

        with col_save:
            if st.button("💾 Save Records to SQLite", type="primary", use_container_width=True):
                try:
                    inserted, skipped = save_to_database(df_uploaded)
                    st.success(f"Database Updated: **{inserted:,}** records inserted, **{skipped:,}** duplicate records skipped.")
                    # Refresh active dataset in session state
                    st.session_state["sales_data"] = load_from_database()
                    st.session_state["filtered_data"] = st.session_state["sales_data"].copy()
                except Exception as e:
                    st.error(f"Database error: {e}")

        with col_clear:
            if st.button("🗑️ Clear Database Records", use_container_width=True):
                clear_database()
                st.session_state["sales_data"] = pd.DataFrame()
                st.session_state["filtered_data"] = pd.DataFrame()
                st.warning("All records cleared from SQLite database.")

else:
    # If no file uploaded, show current database status and option to load sample
    st.info("ℹ️ No new file uploaded. Displaying current active SQLite database records.")
    
    current_df = load_from_database()
    summary = get_table_summary()

    c1, c2, c3 = st.columns(3)
    c1.metric("SQLite Stored Records", f"{summary['total_records']:,}")
    c2.metric("Date Span", f"{summary['first_date'] or 'N/A'} to {summary['last_date'] or 'N/A'}")
    c3.metric("Gross Sales Stored", f"${summary['total_sales']:,.2f}")

    if not current_df.empty:
        st.subheader("Current Active Records")
        st.dataframe(current_df.head(25), use_container_width=True)
    else:
        st.warning("Database is currently empty. Click below to load the built-in sample sales dataset.")
        if st.button("📥 Load Built-in Sample Dataset"):
            from generate_dataset import generate_sales_data
            df_sample = generate_sales_data(1250)
            save_to_database(df_sample)
            st.session_state["sales_data"] = load_from_database()
            st.session_state["filtered_data"] = st.session_state["sales_data"].copy()
            st.success("Loaded 1,250 sample records into SQLite!")
            st.rerun()

# --------------------------------------------------
# Download Center
# --------------------------------------------------
st.markdown("---")
st.subheader("📥 Export Options")
target_export_df = df_uploaded if (df_uploaded is not None and not df_uploaded.empty) else st.session_state.get("sales_data", pd.DataFrame())

if not target_export_df.empty:
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.download_button(
            label="⬇️ Download Data as CSV",
            data=export_to_csv(target_export_df),
            file_name="sales_dataset_export.csv",
            mime="text/csv",
            use_container_width=True
        )
    with dcol2:
        st.download_button(
            label="⬇️ Download Data as Excel (.xlsx)",
            data=export_to_excel(target_export_df),
            file_name="sales_dataset_export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
