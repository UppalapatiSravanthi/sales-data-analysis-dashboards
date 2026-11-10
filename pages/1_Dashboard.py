"""
====================================================================
Page 1: Executive Sales Dashboard
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from database import get_active_dataset
from data_analysis import (
    calculate_kpis,
    generate_business_insights,
    profit_and_loss_analysis
)
from visualization import (
    plot_sales_by_product_bar,
    plot_monthly_sales_trend,
    plot_category_sales_pie,
    plot_region_sales_donut,
    plot_sales_vs_profit_scatter,
    plot_sales_distribution_histogram
)

st.set_page_config(page_title="Executive Dashboard", page_icon="📊", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ensure data is ready
if "sales_data" not in st.session_state or st.session_state["sales_data"] is None or st.session_state["sales_data"].empty:
    st.session_state["sales_data"] = get_active_dataset()

df_raw = st.session_state["sales_data"]

# Sidebar filters
st.sidebar.title("🎛️ Dashboard Filters")

if df_raw is not None and not df_raw.empty:
    df_filtered = df_raw.copy()
    if "Order Date" in df_filtered.columns:
        df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])
        min_d = df_filtered["Order Date"].min().date()
        max_d = df_filtered["Order Date"].max().date()
        dr = st.sidebar.date_input("Date Range", (min_d, max_d), min_value=min_d, max_value=max_d)
        if isinstance(dr, tuple) and len(dr) == 2:
            df_filtered = df_filtered[(df_filtered["Order Date"].dt.date >= dr[0]) & (df_filtered["Order Date"].dt.date <= dr[1])]

    if "Category" in df_filtered.columns:
        cats = sorted(df_raw["Category"].dropna().unique().tolist())
        sel_cats = st.sidebar.multiselect("Category", cats, default=cats)
        if sel_cats:
            df_filtered = df_filtered[df_filtered["Category"].isin(sel_cats)]

    if "Region" in df_filtered.columns:
        regs = sorted(df_raw["Region"].dropna().unique().tolist())
        sel_regs = st.sidebar.multiselect("Region", regs, default=regs)
        if sel_regs:
            df_filtered = df_filtered[df_filtered["Region"].isin(sel_regs)]

    if "Total Sales" in df_filtered.columns and not df_filtered.empty:
        min_s = float(df_raw["Total Sales"].min())
        max_s = float(df_raw["Total Sales"].max())
        s_range = st.sidebar.slider("Sales Amount ($)", round(min_s, 2), round(max_s, 2), (round(min_s, 2), round(max_s, 2)))
        df_filtered = df_filtered[(df_filtered["Total Sales"] >= s_range[0]) & (df_filtered["Total Sales"] <= s_range[1])]

    st.session_state["filtered_data"] = df_filtered
else:
    df_filtered = pd.DataFrame()

st.markdown("<h1 class='page-title'>📊 Executive Sales Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Real-time aggregated KPIs, revenue breakdown, and profitability analytics.</p>", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ No records match current filter criteria. Adjust the filters in the sidebar.")
else:
    # --------------------------------------------------
    # 1. KPI Cards Row
    # --------------------------------------------------
    kpis = calculate_kpis(df_filtered)

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
                <div class="kpi-title">Total Profit</div>
                <div class="kpi-value">${kpis['total_profit']:,.2f}</div>
                <div class="kpi-subtext">{kpis['profitable_orders_pct']}% Orders Profitable</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="kpi-card kpi-card-purple">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">{kpis['total_orders']:,}</div>
                <div class="kpi-subtext">Unique Invoices</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="kpi-card kpi-card-amber">
                <div class="kpi-title">Products Sold</div>
                <div class="kpi-value">{kpis['total_products_sold']:,}</div>
                <div class="kpi-subtext">Units Dispatched</div>
            </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
            <div class="kpi-card kpi-card-cyan">
                <div class="kpi-title">Avg Order Value</div>
                <div class="kpi-value">${kpis['average_order_value']:,.2f}</div>
                <div class="kpi-subtext">Revenue / Order</div>
            </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
            <div class="kpi-card kpi-card-rose">
                <div class="kpi-title">Profit Margin</div>
                <div class="kpi-value">{kpis['profit_margin_pct']}%</div>
                <div class="kpi-subtext">Margin Ratio</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # 2. Charts Row 1: Monthly Trends & Category Share
    # --------------------------------------------------
    r1_col1, r1_col2 = st.columns([1.6, 1.0])
    with r1_col1:
        st.plotly_chart(plot_monthly_sales_trend(df_filtered), use_container_width=True)
    with r1_col2:
        st.plotly_chart(plot_category_sales_pie(df_filtered), use_container_width=True)

    # --------------------------------------------------
    # 3. Charts Row 2: Regional Donut & Top Products Bar
    # --------------------------------------------------
    r2_col1, r2_col2 = st.columns([1.0, 1.6])
    with r2_col1:
        st.plotly_chart(plot_region_sales_donut(df_filtered), use_container_width=True)
    with r2_col2:
        st.plotly_chart(plot_sales_by_product_bar(df_filtered, top_n=8), use_container_width=True)

    # --------------------------------------------------
    # 4. Charts Row 3: Sales vs Profit Scatter & Sales Distribution
    # --------------------------------------------------
    r3_col1, r3_col2 = st.columns([1.3, 1.1])
    with r3_col1:
        st.plotly_chart(plot_sales_vs_profit_scatter(df_filtered), use_container_width=True)
    with r3_col2:
        st.plotly_chart(plot_sales_distribution_histogram(df_filtered), use_container_width=True)

    # --------------------------------------------------
    # 5. Business Insights Grid
    # --------------------------------------------------
    st.subheader("📌 Key Executive Insights")
    insights = generate_business_insights(df_filtered)
    
    in_col1, in_col2 = st.columns(2)
    for idx, ins in enumerate(insights):
        col = in_col1 if (idx % 2 == 0) else in_col2
        with col:
            st.markdown(f"""
                <div class="insight-card">
                    <strong>{ins['title']}</strong><br/>
                    {ins['text']}
                </div>
            """, unsafe_allow_html=True)
