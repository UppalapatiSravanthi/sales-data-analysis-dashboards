"""
====================================================================
Sales Data Analysis and Visualization Dashboard
Main Entry Point & Executive Overview
====================================================================
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime

from database import get_active_dataset, get_table_summary
from data_analysis import calculate_kpis, generate_business_insights
from visualization import plot_monthly_sales_trend, plot_category_sales_pie


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Load Custom CSS Styling
# --------------------------------------------------
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --------------------------------------------------
# Data Initialization
# --------------------------------------------------
if "sales_data" not in st.session_state or st.session_state["sales_data"] is None or st.session_state["sales_data"].empty:
    with st.spinner("Connecting to SQLite database and loading sales records..."):
        st.session_state["sales_data"] = get_active_dataset()


# --------------------------------------------------
# Sidebar: Persistent Interactive Filters
# --------------------------------------------------
st.sidebar.title("🔍 Sales Filters")
st.sidebar.markdown("Use these filters to dynamically slice data across all charts and KPIs.")

df_raw = st.session_state["sales_data"]

if df_raw is not None and not df_raw.empty:
    df_filtered = df_raw.copy()
    
    # 1. Date Range Filter
    if "Order Date" in df_filtered.columns:
        df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])
        min_date = df_filtered["Order Date"].min().date()
        max_date = df_filtered["Order Date"].max().date()
        
        date_range = st.sidebar.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
            df_filtered = df_filtered[
                (df_filtered["Order Date"].dt.date >= start_d) &
                (df_filtered["Order Date"].dt.date <= end_d)
            ]

    # 2. Category Filter
    if "Category" in df_filtered.columns:
        all_categories = sorted(df_raw["Category"].dropna().unique().tolist())
        selected_categories = st.sidebar.multiselect(
            "🏷️ Product Category",
            options=all_categories,
            default=all_categories
        )
        if selected_categories:
            df_filtered = df_filtered[df_filtered["Category"].isin(selected_categories)]

    # 3. Region Filter
    if "Region" in df_filtered.columns:
        all_regions = sorted(df_raw["Region"].dropna().unique().tolist())
        selected_regions = st.sidebar.multiselect(
            "🌍 Sales Region",
            options=all_regions,
            default=all_regions
        )
        if selected_regions:
            df_filtered = df_filtered[df_filtered["Region"].isin(selected_regions)]

    # 4. Product Name Filter
    if "Product Name" in df_filtered.columns:
        all_products = sorted(df_filtered["Product Name"].dropna().unique().tolist())
        selected_products = st.sidebar.multiselect(
            "📦 Specific Product",
            options=all_products,
            default=[]
        )
        if selected_products:
            df_filtered = df_filtered[df_filtered["Product Name"].isin(selected_products)]

    # 5. Sales Amount Range Slider
    if "Total Sales" in df_filtered.columns and not df_filtered.empty:
        min_sales = float(df_raw["Total Sales"].min())
        max_sales = float(df_raw["Total Sales"].max())
        sales_range = st.sidebar.slider(
            "💵 Sales Value Range ($)",
            min_value=round(min_sales, 2),
            max_value=round(max_sales, 2),
            value=(round(min_sales, 2), round(max_sales, 2))
        )
        df_filtered = df_filtered[
            (df_filtered["Total Sales"] >= sales_range[0]) &
            (df_filtered["Total Sales"] <= sales_range[1])
        ]

    st.session_state["filtered_data"] = df_filtered

    # Database Summary Info in Sidebar
    st.sidebar.markdown("---")
    db_summary = get_table_summary()
    st.sidebar.caption(f"💾 **SQLite Database Status:**")
    st.sidebar.caption(f"• Total Saved Records: {db_summary['total_records']:,}")
    st.sidebar.caption(f"• Active Filtered Rows: {len(df_filtered):,}")

    if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
        st.session_state["filtered_data"] = df_raw.copy()
        st.rerun()

else:
    st.session_state["filtered_data"] = pd.DataFrame()


# --------------------------------------------------
# Main Content: Welcome & Executive Overview
# --------------------------------------------------
st.markdown("<h1 class='page-title'>📊 Sales Data Analysis & Visualization Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Interactive business intelligence, sales metrics tracking, and exploratory analysis powered by Python, Streamlit, and SQLite.</p>", unsafe_allow_html=True)

df_active = st.session_state.get("filtered_data", pd.DataFrame())

if df_active is None or df_active.empty:
    st.warning("⚠️ No sales records found matching the active filter criteria. Please adjust filters in the sidebar.")
else:
    # --------------------------------------------------
    # Executive KPI Cards
    # --------------------------------------------------
    kpis = calculate_kpis(df_active)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Sales Revenue</div>
                <div class="kpi-value">${kpis['total_sales']:,.2f}</div>
                <div class="kpi-subtext">Across {kpis['total_orders']:,} Orders</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="kpi-card kpi-card-green">
                <div class="kpi-title">Total Net Profit</div>
                <div class="kpi-value">${kpis['total_profit']:,.2f}</div>
                <div class="kpi-subtext">{kpis['profitable_orders_pct']}% Profitable</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="kpi-card kpi-card-purple">
                <div class="kpi-title">Profit Margin</div>
                <div class="kpi-value">{kpis['profit_margin_pct']}%</div>
                <div class="kpi-subtext">Return on Revenue</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="kpi-card kpi-card-cyan">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">{kpis['total_orders']:,}</div>
                <div class="kpi-subtext">Unique Transactions</div>
            </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
            <div class="kpi-card kpi-card-amber">
                <div class="kpi-title">Products Sold</div>
                <div class="kpi-value">{kpis['total_products_sold']:,}</div>
                <div class="kpi-subtext">Total Units Dispatched</div>
            </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
            <div class="kpi-card kpi-card-rose">
                <div class="kpi-title">Avg Order Value</div>
                <div class="kpi-value">${kpis['average_order_value']:,.2f}</div>
                <div class="kpi-subtext">Revenue per Order</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # Executive Visual Snapshot
    # --------------------------------------------------
    col_chart1, col_chart2 = st.columns([1.6, 1.0])

    with col_chart1:
        st.plotly_chart(plot_monthly_sales_trend(df_active), use_container_width=True)

    with col_chart2:
        st.plotly_chart(plot_category_sales_pie(df_active), use_container_width=True)

    # --------------------------------------------------
    # Key Business Insights Banner
    # --------------------------------------------------
    st.subheader("💡 Key Calculated Business Highlights")
    insights = generate_business_insights(df_active)
    
    col_ins1, col_ins2 = st.columns(2)
    for i, ins in enumerate(insights[:4]):
        target_col = col_ins1 if (i % 2 == 0) else col_ins2
        with target_col:
            st.markdown(f"""
                <div class="insight-card">
                    <strong>{ins['title']}</strong><br/>
                    {ins['text']}
                </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------
    # Feature Navigation Hub
    # --------------------------------------------------
    st.markdown("<hr style='margin: 2rem 0;' />", unsafe_allow_html=True)
    st.subheader("🧭 Navigate Dashboard Features")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.info("📊 **Executive Dashboard (`pages/1_Dashboard.py`)**\n\nFull multi-metric business cockpit with interactive Plotly graphs and distribution metrics.")
        st.success("📁 **Data Upload (`pages/2_Data_Upload.py`)**\n\nUpload custom CSV or Excel files, review schema, data types, and persist to SQLite.")

    with g2:
        st.warning("🧹 **Data Cleaning (`pages/3_Data_Cleaning.py`)**\n\nHandle missing values, eliminate duplicates, enforce formulas, and download cleaned datasets.")
        st.info("📈 **Sales Analysis (`pages/4_Sales_Analysis.py`)**\n\nIn-depth breakdowns: Monthly, Yearly, Product-wise, Category, Regional, and Customer statistics.")

    with g3:
        st.success("🎨 **Data Visualization (`pages/5_Visualization.py`)**\n\nBar charts, Donut charts, Scatter plots, Histograms, Heatmaps, and Matplotlib reports.")
        st.info("📑 **Reports & About (`pages/6_Reports.py` & `pages/7_About.py`)**\n\nExport multi-tab Excel files, download CSVs, view mathematical findings and complete project documentation.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
    <div class="dashboard-footer">
        Sales Data Analysis and Visualization Dashboard &bull; Built with Python, Pandas, Plotly &amp; Streamlit &bull; 100% Deterministic Statistical Analysis
    </div>
""", unsafe_allow_html=True)
