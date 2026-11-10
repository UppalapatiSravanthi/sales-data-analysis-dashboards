"""
Data Analysis and Business Statistics Module
-------------------------------------------
Focuses strictly on Exploratory Data Analysis (EDA), Descriptive Statistics,
and Business Aggregations without any Machine Learning or Predictive Modeling.

Provides:
- Core KPI calculations
- Monthly & Yearly trend analysis with growth rates
- Product, Category, Regional, and Customer breakdowns
- Profit & Loss breakdowns
- Top 10 Best Sellers & Top 10 Profit Generators
- Lowest Performing Products
- Descriptive Statistical Summaries
- Rigorous, calculation-based automated Business Insights
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate high-level Key Performance Indicators (KPIs) for executive dashboards.

    Returns:
        dict: Total Sales, Total Profit, Total Orders, Total Products Sold,
              Average Order Value (AOV), and Profit Margin (%).
    """
    if df is None or df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "total_orders": 0,
            "total_products_sold": 0,
            "average_order_value": 0.0,
            "profit_margin_pct": 0.0,
            "profitable_orders_pct": 0.0
        }

    total_sales = float(df["Total Sales"].sum()) if "Total Sales" in df.columns else 0.0
    total_profit = float(df["Profit"].sum()) if "Profit" in df.columns else 0.0
    total_orders = int(df["Order ID"].nunique()) if "Order ID" in df.columns else len(df)
    total_products_sold = int(df["Quantity"].sum()) if "Quantity" in df.columns else 0
    
    avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0.0
    profit_margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

    profitable_orders = len(df[df["Profit"] > 0]) if "Profit" in df.columns else 0
    profitable_orders_pct = (profitable_orders / len(df) * 100) if len(df) > 0 else 0.0

    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": total_orders,
        "total_products_sold": total_products_sold,
        "average_order_value": round(avg_order_value, 2),
        "profit_margin_pct": round(profit_margin_pct, 2),
        "profitable_orders_pct": round(profitable_orders_pct, 2)
    }


def monthly_sales_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate sales, profit, and order volume by Month.
    Calculates month-over-month growth rate.
    """
    if df is None or df.empty or "Order Date" not in df.columns:
        return pd.DataFrame()

    df_copy = df.copy()
    df_copy["Order Date"] = pd.to_datetime(df_copy["Order Date"])
    df_copy["YearMonth"] = df_copy["Order Date"].dt.to_period("M").astype(str)

    monthly = df_copy.groupby("YearMonth").agg(
        Total_Sales=("Total Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Order_Count=("Order ID", "nunique"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()

    monthly["Sales_Growth_Pct"] = monthly["Total_Sales"].pct_change().fillna(0) * 100
    monthly["Profit_Margin_Pct"] = (monthly["Total_Profit"] / monthly["Total_Sales"] * 100).fillna(0)

    # Format numeric values
    monthly["Total_Sales"] = monthly["Total_Sales"].round(2)
    monthly["Total_Profit"] = monthly["Total_Profit"].round(2)
    monthly["Sales_Growth_Pct"] = monthly["Sales_Growth_Pct"].round(2)
    monthly["Profit_Margin_Pct"] = monthly["Profit_Margin_Pct"].round(2)

    return monthly


def yearly_sales_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales, profit, and order metrics by Year with YoY growth."""
    if df is None or df.empty or "Order Date" not in df.columns:
        return pd.DataFrame()

    df_copy = df.copy()
    df_copy["Order Date"] = pd.to_datetime(df_copy["Order Date"])
    df_copy["Year"] = df_copy["Order Date"].dt.year

    yearly = df_copy.groupby("Year").agg(
        Total_Sales=("Total Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Order_Count=("Order ID", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Average_Order_Value=("Total Sales", "mean")
    ).reset_index()

    yearly["YoY_Sales_Growth_Pct"] = yearly["Total_Sales"].pct_change().fillna(0) * 100
    yearly["Profit_Margin_Pct"] = (yearly["Total_Profit"] / yearly["Total_Sales"] * 100).fillna(0)

    yearly["Total_Sales"] = yearly["Total_Sales"].round(2)
    yearly["Total_Profit"] = yearly["Total_Profit"].round(2)
    yearly["YoY_Sales_Growth_Pct"] = yearly["YoY_Sales_Growth_Pct"].round(2)
    yearly["Profit_Margin_Pct"] = yearly["Profit_Margin_Pct"].round(2)
    yearly["Average_Order_Value"] = yearly["Average_Order_Value"].round(2)

    return yearly


def product_sales_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze sales performance across distinct products."""
    if df is None or df.empty or "Product Name" not in df.columns:
        return pd.DataFrame()

    prod = df.groupby(["Product Name", "Category"]).agg(
        Total_Sales=("Total Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum"),
        Order_Count=("Order ID", "count"),
        Avg_Unit_Price=("Unit Price", "mean")
    ).reset_index()

    prod["Profit_Margin_Pct"] = (prod["Total_Profit"] / prod["Total_Sales"] * 100).fillna(0).round(2)
    prod["Total_Sales"] = prod["Total_Sales"].round(2)
    prod["Total_Profit"] = prod["Total_Profit"].round(2)
    prod["Avg_Unit_Price"] = prod["Avg_Unit_Price"].round(2)

    return prod.sort_values(by="Total_Sales", ascending=False).reset_index(drop=True)


def category_sales_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Breakdown sales, profit, and percentage contribution by Product Category."""
    if df is None or df.empty or "Category" not in df.columns:
        return pd.DataFrame()

    cat = df.groupby("Category").agg(
        Total_Sales=("Total Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum"),
        Order_Count=("Order ID", "count")
    ).reset_index()

    total_revenue = cat["Total_Sales"].sum()
    cat["Revenue_Share_Pct"] = ((cat["Total_Sales"] / total_revenue) * 100).round(2) if total_revenue > 0 else 0
    cat["Profit_Margin_Pct"] = ((cat["Total_Profit"] / cat["Total_Sales"]) * 100).round(2)
    cat["Total_Sales"] = cat["Total_Sales"].round(2)
    cat["Total_Profit"] = cat["Total_Profit"].round(2)

    return cat.sort_values(by="Total_Sales", ascending=False).reset_index(drop=True)


def region_sales_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze sales and profitability across geographical regions."""
    if df is None or df.empty or "Region" not in df.columns:
        return pd.DataFrame()

    reg = df.groupby("Region").agg(
        Total_Sales=("Total Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum"),
        Order_Count=("Order ID", "count")
    ).reset_index()

    total_rev = reg["Total_Sales"].sum()
    reg["Sales_Share_Pct"] = ((reg["Total_Sales"] / total_rev) * 100).round(2) if total_rev > 0 else 0
    reg["Profit_Margin_Pct"] = ((reg["Total_Profit"] / reg["Total_Sales"]) * 100).round(2)
    reg["Total_Sales"] = reg["Total_Sales"].round(2)
    reg["Total_Profit"] = reg["Total_Profit"].round(2)

    return reg.sort_values(by="Total_Sales", ascending=False).reset_index(drop=True)


def customer_sales_analysis(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Identify top individual customers by revenue and order frequency."""
    if df is None or df.empty or "Customer Name" not in df.columns:
        return pd.DataFrame()

    cust = df.groupby("Customer Name").agg(
        Total_Spent=("Total Sales", "sum"),
        Total_Profit_Generated=("Profit", "sum"),
        Orders_Placed=("Order ID", "nunique"),
        Total_Items_Bought=("Quantity", "sum")
    ).reset_index()

    cust["Avg_Order_Value"] = (cust["Total_Spent"] / cust["Orders_Placed"]).round(2)
    cust["Total_Spent"] = cust["Total_Spent"].round(2)
    cust["Total_Profit_Generated"] = cust["Total_Profit_Generated"].round(2)

    return cust.sort_values(by="Total_Spent", ascending=False).head(top_n).reset_index(drop=True)


def profit_and_loss_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Examine profitability distributions, profitable vs loss transactions."""
    if df is None or df.empty or "Profit" not in df.columns:
        return {"profitable_count": 0, "loss_count": 0, "total_loss": 0.0, "total_profit": 0.0}

    profitable_df = df[df["Profit"] >= 0]
    loss_df = df[df["Profit"] < 0]

    return {
        "profitable_transactions": len(profitable_df),
        "loss_transactions": len(loss_df),
        "profitable_pct": round((len(profitable_df) / len(df) * 100), 2),
        "loss_pct": round((len(loss_df) / len(df) * 100), 2),
        "gross_positive_profit": round(float(profitable_df["Profit"].sum()), 2),
        "total_losses_incurred": round(abs(float(loss_df["Profit"].sum())), 2),
        "net_profit": round(float(df["Profit"].sum()), 2)
    }


def top_10_best_selling_products(df: pd.DataFrame, by: str = "Total Sales") -> pd.DataFrame:
    """Return top 10 best-selling products by Total Sales or Quantity."""
    prod = product_sales_analysis(df)
    if prod.empty:
        return pd.DataFrame()
    sort_col = "Total_Sales" if by == "Total Sales" else "Units_Sold"
    return prod.sort_values(by=sort_col, ascending=False).head(10).reset_index(drop=True)


def top_10_highest_profit_products(df: pd.DataFrame) -> pd.DataFrame:
    """Return top 10 products generating the greatest absolute profit."""
    prod = product_sales_analysis(df)
    if prod.empty:
        return pd.DataFrame()
    return prod.sort_values(by="Total_Profit", ascending=False).head(10).reset_index(drop=True)


def lowest_performing_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Identify products with the lowest overall revenue contribution."""
    prod = product_sales_analysis(df)
    if prod.empty:
        return pd.DataFrame()
    return prod.sort_values(by="Total_Sales", ascending=True).head(n).reset_index(drop=True)


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute mathematical descriptive statistics on numeric columns."""
    if df is None or df.empty:
        return pd.DataFrame()

    numeric_cols = [c for c in ["Quantity", "Unit Price", "Total Sales", "Cost", "Profit"] if c in df.columns]
    if not numeric_cols:
        return pd.DataFrame()

    desc = df[numeric_cols].describe().T
    desc = desc.rename(columns={
        "count": "Count",
        "mean": "Mean",
        "std": "Std Dev",
        "min": "Minimum",
        "25%": "25th Percentile",
        "50%": "Median (50%)",
        "75%": "75th Percentile",
        "max": "Maximum"
    })
    
    # Add median and variance explicitly
    desc["Median"] = df[numeric_cols].median()
    desc["Variance"] = df[numeric_cols].var().round(2)
    
    return desc.round(2)


def generate_business_insights(df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Generate authentic, data-driven executive insights derived strictly from
    actual mathematical calculations on the dataset.
    """
    if df is None or df.empty:
        return [{"title": "No Data", "text": "Insufficient data available to formulate insights."}]

    insights = []
    kpis = calculate_kpis(df)
    cat_df = category_sales_analysis(df)
    reg_df = region_sales_analysis(df)
    prod_df = product_sales_analysis(df)
    monthly_df = monthly_sales_analysis(df)
    pnl = profit_and_loss_analysis(df)

    # 1. Top Category Revenue Contributor
    if not cat_df.empty:
        top_cat = cat_df.iloc[0]
        insights.append({
            "title": f"Leading Category: {top_cat['Category']}",
            "text": f"{top_cat['Category']} is the primary revenue driver, generating ${top_cat['Total_Sales']:,.2f} "
                    f"({top_cat['Revenue_Share_Pct']}% of total sales) with a profit margin of {top_cat['Profit_Margin_Pct']}%."
        })

    # 2. Top Performing Region
    if not reg_df.empty:
        top_reg = reg_df.iloc[0]
        insights.append({
            "title": f"Top Geographical Region: {top_reg['Region']}",
            "text": f"The {top_reg['Region']} region leads company operations, accounting for ${top_reg['Total_Sales']:,.2f} "
                    f"in revenue and ${top_reg['Total_Profit']:,.2f} in net profit ({top_reg['Sales_Share_Pct']}% regional share)."
        })

    # 3. Best Performing Product
    if not prod_df.empty:
        best_prod = prod_df.iloc[0]
        insights.append({
            "title": f"Highest Grossing Product: {best_prod['Product Name']}",
            "text": f"'{best_prod['Product Name']}' generated the highest revenue at ${best_prod['Total_Sales']:,.2f} "
                    f"across {best_prod['Units_Sold']} units sold, delivering ${best_prod['Total_Profit']:,.2f} in profit."
        })

    # 4. Highest Profit Margin Product
    if not prod_df.empty:
        highest_margin_prod = prod_df.sort_values(by="Profit_Margin_Pct", ascending=False).iloc[0]
        insights.append({
            "title": f"Highest Margin Product: {highest_margin_prod['Product Name']}",
            "text": f"'{highest_margin_prod['Product Name']}' yields the highest profit efficiency with an impressive "
                    f"{highest_margin_prod['Profit_Margin_Pct']}% profit margin."
        })

    # 5. Peak Sales Month
    if not monthly_df.empty:
        peak_month = monthly_df.sort_values(by="Total_Sales", ascending=False).iloc[0]
        insights.append({
            "title": f"Peak Sales Period: {peak_month['YearMonth']}",
            "text": f"The strongest operating month on record was {peak_month['YearMonth']} with ${peak_month['Total_Sales']:,.2f} "
                    f"in gross revenue and ${peak_month['Total_Profit']:,.2f} in profit across {peak_month['Order_Count']} orders."
        })

    # 6. Overall Profitability Ratio
    insights.append({
        "title": f"Healthy Overall Margin: {kpis['profit_margin_pct']}%",
        "text": f"Out of ${kpis['total_sales']:,.2f} in total gross sales, the company secured ${kpis['total_profit']:,.2f} "
                f"in net profit, reflecting an overall profit margin of {kpis['profit_margin_pct']}%. "
                f"{kpis['profitable_orders_pct']}% of all recorded orders were profitable."
    })

    # 7. Loss and Clearance Transactions
    if pnl["loss_transactions"] > 0:
        insights.append({
            "title": f"Loss Mitigation Opportunity ({pnl['loss_transactions']} Orders)",
            "text": f"A total of {pnl['loss_transactions']} orders ({pnl['loss_pct']}% of transactions) recorded negative profit, "
                    f"incurring ${pnl['total_losses_incurred']:,.2f} in discounts or clearance losses. Restricting heavy discounting "
                    f"could directly recover this revenue."
        })

    # 8. Average Order Value
    insights.append({
        "title": f"Average Basket Size: ${kpis['average_order_value']:,.2f}",
        "text": f"Across {kpis['total_orders']:,} distinct orders, customers purchased an average of "
                f"{round(kpis['total_products_sold'] / kpis['total_orders'], 1) if kpis['total_orders'] > 0 else 0} items per transaction, "
                f"resulting in an Average Order Value (AOV) of ${kpis['average_order_value']:,.2f}."
    })

    return insights
