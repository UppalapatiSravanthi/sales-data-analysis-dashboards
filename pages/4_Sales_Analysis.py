"""
====================================================================
Page 4: Detailed Sales and Statistical Analysis
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from database import get_active_dataset
from data_analysis import (
    monthly_sales_analysis,
    yearly_sales_analysis,
    product_sales_analysis,
    category_sales_analysis,
    region_sales_analysis,
    customer_sales_analysis,
    profit_and_loss_analysis,
    top_10_best_selling_products,
    top_10_highest_profit_products,
    lowest_performing_products,
    descriptive_statistics
)

st.set_page_config(page_title="Sales Analysis", page_icon="📈", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ensure base dataset is available
if "sales_data" not in st.session_state or st.session_state["sales_data"] is None or st.session_state["sales_data"].empty:
    st.session_state["sales_data"] = get_active_dataset()

df_active = st.session_state.get("filtered_data", st.session_state["sales_data"])

st.markdown("<h1 class='page-title'>📈 Comprehensive Sales & Statistical Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Deterministic exploratory breakdowns: temporal growth, product rankings, regional metrics, and statistical distributions.</p>", unsafe_allow_html=True)

if df_active is None or df_active.empty:
    st.warning("⚠️ No data available to analyze. Please adjust filters or ingest records.")
else:
    # --------------------------------------------------
    # Analysis Tabs
    # --------------------------------------------------
    tabs = st.tabs([
        "📅 Monthly & Yearly Trends",
        "🏆 Product Rankings",
        "🏷️ Category & Region Analysis",
        "👥 Customer Analytics",
        "⚖️ Profit & Loss Breakdown",
        "📐 Descriptive Statistics"
    ])

    # Tab 1: Temporal Analysis
    with tabs[0]:
        st.subheader("Monthly Performance & MoM Growth")
        monthly_df = monthly_sales_analysis(df_active)
        if not monthly_df.empty:
            st.dataframe(monthly_df.style.format({
                "Total_Sales": "${:,.2f}",
                "Total_Profit": "${:,.2f}",
                "Order_Count": "{:,}",
                "Units_Sold": "{:,}",
                "Sales_Growth_Pct": "{:+.2f}%",
                "Profit_Margin_Pct": "{:.2f}%"
            }), use_container_width=True)
        else:
            st.info("No monthly timeline data.")

        st.markdown("---")
        st.subheader("Yearly Performance & YoY Growth")
        yearly_df = yearly_sales_analysis(df_active)
        if not yearly_df.empty:
            st.dataframe(yearly_df.style.format({
                "Total_Sales": "${:,.2f}",
                "Total_Profit": "${:,.2f}",
                "Order_Count": "{:,}",
                "Units_Sold": "{:,}",
                "Average_Order_Value": "${:,.2f}",
                "YoY_Sales_Growth_Pct": "{:+.2f}%",
                "Profit_Margin_Pct": "{:.2f}%"
            }), use_container_width=True)

    # Tab 2: Product Performance Rankings
    with tabs[1]:
        pcol1, pcol2 = st.columns(2)
        
        with pcol1:
            st.markdown("### 🥇 Top 10 Best-Selling Products (Revenue)")
            top_sales_df = top_10_best_selling_products(df_active, by="Total Sales")
            st.dataframe(top_sales_df[["Product Name", "Category", "Total_Sales", "Units_Sold", "Profit_Margin_Pct"]].style.format({
                "Total_Sales": "${:,.2f}",
                "Units_Sold": "{:,}",
                "Profit_Margin_Pct": "{:.2f}%"
            }), use_container_width=True)

        with pcol2:
            st.markdown("### 💰 Top 10 Highest-Profit Products")
            top_profit_df = top_10_highest_profit_products(df_active)
            st.dataframe(top_profit_df[["Product Name", "Category", "Total_Profit", "Profit_Margin_Pct", "Total_Sales"]].style.format({
                "Total_Profit": "${:,.2f}",
                "Total_Sales": "${:,.2f}",
                "Profit_Margin_Pct": "{:.2f}%"
            }), use_container_width=True)

        st.markdown("---")
        st.markdown("### ⚠️ Lowest-Performing Products (Revenue)")
        lowest_df = lowest_performing_products(df_active, n=10)
        st.dataframe(lowest_df[["Product Name", "Category", "Total_Sales", "Total_Profit", "Units_Sold"]].style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Units_Sold": "{:,}"
        }), use_container_width=True)

    # Tab 3: Category & Region
    with tabs[2]:
        ccol1, ccol2 = st.columns(2)

        with ccol1:
            st.markdown("### 🏷️ Category Performance Breakdown")
            cat_df = category_sales_analysis(df_active)
            st.dataframe(cat_df.style.format({
                "Total_Sales": "${:,.2f}",
                "Total_Profit": "${:,.2f}",
                "Units_Sold": "{:,}",
                "Order_Count": "{:,}",
                "Revenue_Share_Pct": "{:.2f}%",
                "Profit_Margin_Pct": "{:.2f}%"
            }), use_container_width=True)

        with ccol2:
            st.markdown("### 🌍 Regional Performance Breakdown")
            reg_df = region_sales_analysis(df_active)
            st.dataframe(reg_df.style.format({
                "Total_Sales": "${:,.2f}",
                "Total_Profit": "${:,.2f}",
                "Units_Sold": "{:,}",
                "Order_Count": "{:,}",
                "Sales_Share_Pct": "{:.2f}%",
                "Profit_Margin_Pct": "{:.2f}%"
            }), use_container_width=True)

    # Tab 4: Customer Analytics
    with tabs[3]:
        st.subheader("Top 15 Most Valuable Customers")
        cust_df = customer_sales_analysis(df_active, top_n=15)
        st.dataframe(cust_df.style.format({
            "Total_Spent": "${:,.2f}",
            "Total_Profit_Generated": "${:,.2f}",
            "Orders_Placed": "{:,}",
            "Total_Items_Bought": "{:,}",
            "Avg_Order_Value": "${:,.2f}"
        }), use_container_width=True)

    # Tab 5: Profit & Loss Analysis
    with tabs[4]:
        st.subheader("Profitability & Order Health")
        pnl = profit_and_loss_analysis(df_active)

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Profitable Orders", f"{pnl['profitable_transactions']:,}", f"{pnl['profitable_pct']}% of total")
        p2.metric("Loss-Incurring Orders", f"{pnl['loss_transactions']:,}", f"{pnl['loss_pct']}% of total", delta_color="inverse")
        p3.metric("Gross Positive Profit", f"${pnl['gross_positive_profit']:,.2f}")
        p4.metric("Losses Incurred", f"${pnl['total_losses_incurred']:,.2f}", delta_color="inverse")

        st.markdown("---")
        st.markdown("### Clearance & Negative Profit Transactions")
        loss_orders = df_active[df_active["Profit"] < 0]
        if not loss_orders.empty:
            st.dataframe(loss_orders.head(25), use_container_width=True)
        else:
            st.success("🎉 No loss-incurring orders recorded in the current filter selection!")

    # Tab 6: Descriptive Statistics
    with tabs[5]:
        st.subheader("Mathematical Summary & Spread Analysis")
        stats_df = descriptive_statistics(df_active)
        st.dataframe(stats_df, use_container_width=True)
        st.caption("Calculated purely using standard deviation, variance, quartiles, median, and mean without estimation heuristics.")
