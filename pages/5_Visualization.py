"""
====================================================================
Page 5: Interactive Visualizations & Charting Hub
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from database import get_active_dataset
from visualization import (
    plot_sales_by_product_bar,
    plot_monthly_sales_trend,
    plot_category_sales_pie,
    plot_region_sales_donut,
    plot_sales_distribution_histogram,
    plot_sales_vs_profit_scatter,
    plot_monthly_heatmap,
    plot_matplotlib_sales_summary
)

st.set_page_config(page_title="Data Visualizations", page_icon="🎨", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ensure data is ready
if "sales_data" not in st.session_state or st.session_state["sales_data"] is None or st.session_state["sales_data"].empty:
    st.session_state["sales_data"] = get_active_dataset()

df_active = st.session_state.get("filtered_data", st.session_state["sales_data"])

st.markdown("<h1 class='page-title'>🎨 Interactive Visualizations & Charts</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Plotly interactive figures, responsive layouts, drill-downs, and Matplotlib composite reports.</p>", unsafe_allow_html=True)

if df_active is None or df_active.empty:
    st.warning("⚠️ No data available to visualize. Please check active filters.")
else:
    # --------------------------------------------------
    # Visualization Catalog Tabs
    # --------------------------------------------------
    viz_tabs = st.tabs([
        "📊 Bar Chart (Products)",
        "📈 Line Chart (Trends)",
        "🥧 Category & Regional Distribution",
        "📦 Histogram (Distribution)",
        "🔵 Scatter Plot (Sales vs Profit)",
        "🌡️ Heatmap (Monthly Matrix)",
        "🖼️ Matplotlib Composite Report"
    ])

    # Tab 1: Bar Chart
    with viz_tabs[0]:
        st.subheader("Product Revenue Comparison")
        top_n = st.slider("Select Number of Top Products to Display", min_value=5, max_value=25, value=10, step=1)
        st.plotly_chart(plot_sales_by_product_bar(df_active, top_n=top_n), use_container_width=True)
        st.caption("Hover over bars to inspect exact dollar revenue amounts and product details.")

    # Tab 2: Line Chart
    with viz_tabs[1]:
        st.subheader("Monthly Sales & Profit Performance")
        st.plotly_chart(plot_monthly_sales_trend(df_active), use_container_width=True)
        st.caption("Displays aggregate Monthly Gross Revenue ($) along with Net Profit ($) on a synchronized time axis.")

    # Tab 3: Pie & Donut Charts
    with viz_tabs[2]:
        col_pie, col_donut = st.columns(2)
        with col_pie:
            st.subheader("Category Revenue Share")
            st.plotly_chart(plot_category_sales_pie(df_active), use_container_width=True)
        with col_donut:
            st.subheader("Geographical Distribution")
            st.plotly_chart(plot_region_sales_donut(df_active), use_container_width=True)

    # Tab 4: Histogram
    with viz_tabs[3]:
        st.subheader("Order Size Distribution")
        st.plotly_chart(plot_sales_distribution_histogram(df_active), use_container_width=True)
        st.caption("Shows frequency of transactions across different order dollar amounts.")

    # Tab 5: Scatter Plot
    with viz_tabs[4]:
        st.subheader("Sales vs. Profit Correlation")
        st.plotly_chart(plot_sales_vs_profit_scatter(df_active), use_container_width=True)
        st.caption("Each point represents an individual order. Points below the red dashed line reflect negative profit or discount clearances.")

    # Tab 6: Heatmap
    with viz_tabs[5]:
        st.subheader("Monthly Sales Intensity Heatmap by Category")
        st.plotly_chart(plot_monthly_heatmap(df_active), use_container_width=True)
        st.caption("Darker shades indicate higher total revenue generated in that particular month and category.")

    # Tab 7: Matplotlib Static Report
    with viz_tabs[6]:
        st.subheader("Static Matplotlib Multi-Panel Figure")
        st.write("Ideal for offline reporting, exports, and publication layouts.")
        fig = plot_matplotlib_sales_summary(df_active)
        st.pyplot(fig)
