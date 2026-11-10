"""
====================================================================
Page 6: Executive Reports & Data Export Center
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from database import get_active_dataset
from data_analysis import (
    calculate_kpis,
    generate_business_insights,
    descriptive_statistics,
    category_sales_analysis,
    region_sales_analysis
)
from report_generation import export_to_csv, export_to_excel, generate_text_report

st.set_page_config(page_title="Executive Reports", page_icon="📑", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ensure base dataset is available
if "sales_data" not in st.session_state or st.session_state["sales_data"] is None or st.session_state["sales_data"].empty:
    st.session_state["sales_data"] = get_active_dataset()

df_active = st.session_state.get("filtered_data", st.session_state["sales_data"])

st.markdown("<h1 class='page-title'>📑 Executive Reports & Export Center</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Export certified sales reports, comprehensive multi-sheet Excel workbooks, and mathematical business summaries.</p>", unsafe_allow_html=True)

if df_active is None or df_active.empty:
    st.warning("⚠️ No data currently available to generate a report. Adjust filters to continue.")
else:
    kpis = calculate_kpis(df_active)
    insights = generate_business_insights(df_active)

    # --------------------------------------------------
    # 1. Executive Summary Cards
    # --------------------------------------------------
    st.subheader("1. Key Performance Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gross Revenue", f"${kpis['total_sales']:,.2f}")
    k2.metric("Net Profit", f"${kpis['total_profit']:,.2f}")
    k3.metric("Profit Margin", f"{kpis['profit_margin_pct']}%")
    k4.metric("Total Invoices", f"{kpis['total_orders']:,}")

    # --------------------------------------------------
    # 2. Calculated Business Insights (Real Calculations)
    # --------------------------------------------------
    st.subheader("2. Mathematically Computed Business Insights")
    st.write("All insights below are computed deterministically from real sales aggregations:")

    for idx, item in enumerate(insights, 1):
        st.markdown(f"""
            <div class="insight-card">
                <strong>{idx}. {item['title']}</strong><br/>
                {item['text']}
            </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------
    # 3. Export Formats
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("3. Download Formal Reports")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        st.markdown("#### 📊 Multi-Sheet Excel Workbook")
        st.write("Includes Executive Summary, Raw Filtered Rows, Monthly Analysis, Category, Regional, and Top 10 Product sheets.")
        st.download_button(
            label="⬇️ Download Excel Workbook (.xlsx)",
            data=export_to_excel(df_active),
            file_name="executive_sales_analysis_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )

    with col_btn2:
        st.markdown("#### 📄 Filtered Dataset (CSV)")
        st.write("Exports active filtered rows with all 11 columns suitable for external spreadsheets and business intelligence tools.")
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=export_to_csv(df_active),
            file_name="filtered_sales_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_btn3:
        st.markdown("#### 📝 Executive Markdown Summary")
        st.write("Clean narrative summary containing timestamps, KPI lists, category/region breakdown tables, and key insights.")
        text_report = generate_text_report(df_active)
        st.download_button(
            label="⬇️ Download Markdown Report (.md)",
            data=text_report.encode("utf-8"),
            file_name="executive_sales_summary.md",
            mime="text/markdown",
            use_container_width=True
        )

    # --------------------------------------------------
    # 4. Report Text Preview
    # --------------------------------------------------
    st.markdown("---")
    with st.expander("👁️ Preview Narrative Executive Report"):
        st.markdown(generate_text_report(df_active))
