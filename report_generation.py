"""
Report Generation and Export Module
-----------------------------------
Generates professional downloadable reports in multiple formats:
1. Filtered Data Export (CSV)
2. Multi-Sheet Executive Workbook (Excel - .xlsx)
3. Formatted Executive Summary Report (Markdown/Text)

Ensures all business insights and summary statistics are derived
strictly from real dataset calculations.
"""

import io
from datetime import datetime
import pandas as pd
from typing import Dict, Any, List
from data_analysis import (
    calculate_kpis,
    monthly_sales_analysis,
    category_sales_analysis,
    region_sales_analysis,
    top_10_best_selling_products,
    generate_business_insights
)


def export_to_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to UTF-8 encoded CSV bytes for Streamlit download."""
    if df is None or df.empty:
        return b""
    return df.to_csv(index=False).encode("utf-8")


def export_to_excel(df: pd.DataFrame) -> bytes:
    """
    Generate an Executive Excel Workbook with multiple styled tabs:
    - Tab 1: Executive KPI Summary
    - Tab 2: Raw Filtered Transactions
    - Tab 3: Monthly Breakdown
    - Tab 4: Category Analysis
    - Tab 5: Regional Analysis
    - Tab 6: Top 10 Best Sellers
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Tab 1: Executive KPIs
        kpis = calculate_kpis(df)
        kpi_summary = pd.DataFrame([
            {"Metric": "Report Generation Date", "Value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            {"Metric": "Total Sales Revenue", "Value": f"${kpis['total_sales']:,.2f}"},
            {"Metric": "Total Net Profit", "Value": f"${kpis['total_profit']:,.2f}"},
            {"Metric": "Overall Profit Margin", "Value": f"{kpis['profit_margin_pct']}%"},
            {"Metric": "Total Orders Placed", "Value": f"{kpis['total_orders']:,}"},
            {"Metric": "Total Quantity Sold", "Value": f"{kpis['total_products_sold']:,}"},
            {"Metric": "Average Order Value (AOV)", "Value": f"${kpis['average_order_value']:,.2f}"},
            {"Metric": "Profitable Orders (%)", "Value": f"{kpis['profitable_orders_pct']}%"}
        ])
        kpi_summary.to_excel(writer, sheet_name="Executive Summary", index=False)

        # Tab 2: Filtered Data
        if df is not None and not df.empty:
            df.to_excel(writer, sheet_name="Sales Records", index=False)

        # Tab 3: Monthly Breakdown
        monthly_df = monthly_sales_analysis(df)
        if not monthly_df.empty:
            monthly_df.to_excel(writer, sheet_name="Monthly Analysis", index=False)

        # Tab 4: Category Analysis
        cat_df = category_sales_analysis(df)
        if not cat_df.empty:
            cat_df.to_excel(writer, sheet_name="Category Performance", index=False)

        # Tab 5: Regional Analysis
        reg_df = region_sales_analysis(df)
        if not reg_df.empty:
            reg_df.to_excel(writer, sheet_name="Regional Performance", index=False)

        # Tab 6: Top 10 Products
        top_prod = top_10_best_selling_products(df)
        if not top_prod.empty:
            top_prod.to_excel(writer, sheet_name="Top 10 Products", index=False)

    return output.getvalue()


def generate_text_report(df: pd.DataFrame) -> str:
    """
    Generate an executive narrative report in clean Markdown format,
    complete with mathematical KPIs and computed business insights.
    """
    if df is None or df.empty:
        return "No sales data available to compile a report."

    kpis = calculate_kpis(df)
    insights = generate_business_insights(df)
    cat_df = category_sales_analysis(df)
    reg_df = region_sales_analysis(df)

    date_generated = datetime.now().strftime("%B %d, %Y at %H:%M:%S")

    report_lines = [
        "# EXECUTIVE SALES ANALYSIS REPORT",
        f"**Generated:** {date_generated}",
        f"**Records Analyzed:** {len(df):,} transactions",
        "",
        "---",
        "## 1. Executive Performance Summary",
        f"- **Total Sales Revenue:** ${kpis['total_sales']:,.2f}",
        f"- **Total Net Profit:** ${kpis['total_profit']:,.2f}",
        f"- **Profit Margin:** {kpis['profit_margin_pct']}%",
        f"- **Total Orders Processed:** {kpis['total_orders']:,}",
        f"- **Total Units Sold:** {kpis['total_products_sold']:,}",
        f"- **Average Order Value (AOV):** ${kpis['average_order_value']:,.2f}",
        f"- **Profitable Orders Percentage:** {kpis['profitable_orders_pct']}%",
        "",
        "---",
        "## 2. Category Performance Overview",
    ]

    if not cat_df.empty:
        report_lines.append("| Category | Revenue ($) | Profit ($) | Share (%) | Margin (%) |")
        report_lines.append("|---|---|---|---|---|")
        for _, row in cat_df.iterrows():
            report_lines.append(
                f"| {row['Category']} | ${row['Total_Sales']:,.2f} | ${row['Total_Profit']:,.2f} | "
                f"{row['Revenue_Share_Pct']}% | {row['Profit_Margin_Pct']}% |"
            )

    report_lines.extend([
        "",
        "---",
        "## 3. Geographic Performance Overview",
    ])

    if not reg_df.empty:
        report_lines.append("| Region | Revenue ($) | Profit ($) | Share (%) | Margin (%) |")
        report_lines.append("|---|---|---|---|---|")
        for _, row in reg_df.iterrows():
            report_lines.append(
                f"| {row['Region']} | ${row['Total_Sales']:,.2f} | ${row['Total_Profit']:,.2f} | "
                f"{row['Sales_Share_Pct']}% | {row['Profit_Margin_Pct']}% |"
            )

    report_lines.extend([
        "",
        "---",
        "## 4. Calculated Business Insights",
    ])

    for i, ins in enumerate(insights, 1):
        report_lines.append(f"### {i}. {ins['title']}")
        report_lines.append(f"{ins['text']}")
        report_lines.append("")

    report_lines.extend([
        "---",
        "*Report autonomously synthesized via the Sales Data Analysis and Visualization Engine.*"
    ])

    return "\n".join(report_lines)
