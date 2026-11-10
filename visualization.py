"""
Data Visualization Module
-------------------------
Creates interactive Plotly charts and static Matplotlib figures for
sales and profit exploration.

Visualizations:
- Bar Chart: Sales by Product (Top N)
- Line Chart: Monthly Sales & Profit Trends with markers
- Pie Chart: Category-wise Sales Distribution
- Donut Chart: Region-wise Sales Breakdown
- Histogram: Sales Distribution with frequency curves
- Scatter Plot: Sales vs. Profit colored by Category
- Heatmap: Monthly/Yearly Sales Comparison matrix
- Matplotlib Static Multi-panel Report Figure
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


# Consistent color palettes
CHART_THEME = "plotly_white"
PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#10b981"
ACCENT_COLOR = "#f59e0b"
PALETTE = px.colors.qualitative.Prism


def plot_sales_by_product_bar(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal Bar Chart showing Top N Products by Total Sales."""
    if df is None or df.empty or "Product Name" not in df.columns:
        return go.Figure()

    prod_summary = df.groupby("Product Name")["Total Sales"].sum().reset_index()
    prod_summary = prod_summary.sort_values(by="Total Sales", ascending=True).tail(top_n)

    fig = px.bar(
        prod_summary,
        x="Total Sales",
        y="Product Name",
        orientation="h",
        title=f"Top {top_n} Best-Selling Products by Revenue",
        labels={"Total Sales": "Total Revenue ($)", "Product Name": "Product"},
        color="Total Sales",
        color_continuous_scale="Blues",
        text_auto="$,.2s"
    )

    fig.update_layout(
        template=CHART_THEME,
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor="#e2e8f0"),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False
    )
    return fig


def plot_monthly_sales_trend(df: pd.DataFrame) -> go.Figure:
    """Dual-axis interactive Line Chart showing Monthly Sales & Profit trends."""
    if df is None or df.empty or "Order Date" not in df.columns:
        return go.Figure()

    df_copy = df.copy()
    df_copy["Order Date"] = pd.to_datetime(df_copy["Order Date"])
    df_copy["YearMonth"] = df_copy["Order Date"].dt.to_period("M").astype(str)

    monthly = df_copy.groupby("YearMonth").agg(
        Total_Sales=("Total Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["Total_Sales"],
        mode="lines+markers",
        name="Sales Revenue ($)",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=7, color="#1d4ed8"),
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=monthly["YearMonth"],
        y=monthly["Total_Profit"],
        mode="lines+markers",
        name="Net Profit ($)",
        line=dict(color="#10b981", width=3, dash="dot"),
        marker=dict(size=7, color="#059669"),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        title="Monthly Sales Revenue & Profit Trends",
        template=CHART_THEME,
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode="x unified",
        height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def plot_category_sales_pie(df: pd.DataFrame) -> go.Figure:
    """Pie Chart for Category-wise Sales Breakdown."""
    if df is None or df.empty or "Category" not in df.columns:
        return go.Figure()

    cat_summary = df.groupby("Category")["Total Sales"].sum().reset_index()

    fig = px.pie(
        cat_summary,
        names="Category",
        values="Total Sales",
        title="Sales Revenue Contribution by Category",
        color_discrete_sequence=px.colors.qualitative.Safe,
        hole=0.0
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(
        template=CHART_THEME,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def plot_region_sales_donut(df: pd.DataFrame) -> go.Figure:
    """Donut Chart for Region-wise Sales Breakdown."""
    if df is None or df.empty or "Region" not in df.columns:
        return go.Figure()

    region_summary = df.groupby("Region")["Total Sales"].sum().reset_index()

    fig = px.pie(
        region_summary,
        names="Region",
        values="Total Sales",
        title="Geographic Sales Distribution by Region",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label} Region</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(
        template=CHART_THEME,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def plot_sales_distribution_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram showing distribution of order sales values."""
    if df is None or df.empty or "Total Sales" not in df.columns:
        return go.Figure()

    fig = px.histogram(
        df,
        x="Total Sales",
        nbins=40,
        title="Order Sales Value Distribution",
        labels={"Total Sales": "Order Sales Amount ($)"},
        color_discrete_sequence=["#3b82f6"],
        opacity=0.85
    )
    fig.update_layout(
        template=CHART_THEME,
        height=400,
        yaxis_title="Number of Orders",
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def plot_sales_vs_profit_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter Plot: Sales vs Profit colored by Product Category."""
    if df is None or df.empty or not {"Total Sales", "Profit", "Category"}.issubset(df.columns):
        return go.Figure()

    fig = px.scatter(
        df,
        x="Total Sales",
        y="Profit",
        color="Category",
        size="Quantity" if "Quantity" in df.columns else None,
        hover_data=["Order ID", "Product Name", "Region"] if "Order ID" in df.columns else None,
        title="Order Sales vs. Profit Relationship",
        labels={"Total Sales": "Total Sales ($)", "Profit": "Profit ($)"},
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    # Add zero-profit reference line
    fig.add_hline(y=0, line_dash="dash", line_color="#ef4444", annotation_text="Break-Even Line")

    fig.update_layout(
        template=CHART_THEME,
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
    )
    return fig


def plot_monthly_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap showing Category-wise Sales across Months."""
    if df is None or df.empty or not {"Order Date", "Category", "Total Sales"}.issubset(df.columns):
        return go.Figure()

    df_copy = df.copy()
    df_copy["Order Date"] = pd.to_datetime(df_copy["Order Date"])
    df_copy["YearMonth"] = df_copy["Order Date"].dt.to_period("M").astype(str)

    pivot_table = df_copy.pivot_table(
        index="Category",
        columns="YearMonth",
        values="Total Sales",
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        pivot_table,
        labels=dict(x="Month", y="Category", color="Sales ($)"),
        title="Monthly Sales Heatmap by Category",
        color_continuous_scale="Viridis",
        aspect="auto"
    )

    fig.update_layout(
        template=CHART_THEME,
        height=380,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def plot_matplotlib_sales_summary(df: pd.DataFrame):
    """
    Generate a 2x2 multi-panel static Matplotlib figure suitable for
    visual report generation or printable exports.
    """
    if df is None or df.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "No Data Available", ha="center", va="center")
        return fig

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor("#ffffff")
    plt.subplots_adjust(hspace=0.35, wspace=0.25)

    # 1. Category Bar
    cat = df.groupby("Category")["Total Sales"].sum().sort_values(ascending=False)
    axes[0, 0].bar(cat.index, cat.values, color="#2563eb", edgecolor="#1e40af")
    axes[0, 0].set_title("Sales by Category", fontsize=12, fontweight="bold")
    axes[0, 0].set_ylabel("Sales ($)")
    axes[0, 0].tick_params(axis="x", rotation=15)
    axes[0, 0].grid(axis="y", linestyle="--", alpha=0.5)

    # 2. Region Bar
    reg = df.groupby("Region")["Total Sales"].sum().sort_values(ascending=False)
    axes[0, 1].bar(reg.index, reg.values, color="#10b981", edgecolor="#065f46")
    axes[0, 1].set_title("Sales by Region", fontsize=12, fontweight="bold")
    axes[0, 1].set_ylabel("Sales ($)")
    axes[0, 1].grid(axis="y", linestyle="--", alpha=0.5)

    # 3. Profit Margin by Category
    cat_profit = df.groupby("Category").agg(Sales=("Total Sales", "sum"), Profit=("Profit", "sum"))
    cat_profit["Margin"] = (cat_profit["Profit"] / cat_profit["Sales"]) * 100
    axes[1, 0].barh(cat_profit.index, cat_profit["Margin"], color="#f59e0b", edgecolor="#b45309")
    axes[1, 0].set_title("Profit Margin (%) by Category", fontsize=12, fontweight="bold")
    axes[1, 0].set_xlabel("Margin (%)")
    axes[1, 0].grid(axis="x", linestyle="--", alpha=0.5)

    # 4. Sales Distribution
    axes[1, 1].hist(df["Total Sales"], bins=25, color="#8b5cf6", edgecolor="#5b21b6", alpha=0.85)
    axes[1, 1].set_title("Sales Distribution Histogram", fontsize=12, fontweight="bold")
    axes[1, 1].set_xlabel("Order Amount ($)")
    axes[1, 1].set_ylabel("Frequency")
    axes[1, 1].grid(axis="y", linestyle="--", alpha=0.5)

    return fig
