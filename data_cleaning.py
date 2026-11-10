"""
Data Cleaning and Preprocessing Module
-------------------------------------
Provides beginner-friendly, robust utilities for:
- Inspecting datasets (shapes, missing values, duplicates, dtypes)
- Cleaning and standardizing column names
- Imputing or dropping missing values
- Removing duplicate transactions
- Validating and recalculating mathematical relations (Sales & Profit)
- Converting date formats cleanly
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def inspect_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Inspect a DataFrame and generate summary diagnostics.

    Args:
        df (pd.DataFrame): Input dataset.

    Returns:
        dict: Inspection report containing shape, missing counts, duplicates, types.
    """
    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "column_names": [],
            "dtypes": {},
            "missing_values": {},
            "total_missing": 0,
            "duplicate_rows": 0
        }

    missing_series = df.isnull().sum()
    missing_dict = missing_series[missing_series > 0].to_dict()

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": missing_dict,
        "total_missing": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    }


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize common column naming variations to title case format.
    E.g., 'order_id', 'order id', 'Order ID' -> 'Order ID'
    """
    mapping = {
        "order id": "Order ID",
        "order_id": "Order ID",
        "orderid": "Order ID",
        "order date": "Order Date",
        "order_date": "Order Date",
        "orderdate": "Order Date",
        "date": "Order Date",
        "customer name": "Customer Name",
        "customer_name": "Customer Name",
        "customer": "Customer Name",
        "product name": "Product Name",
        "product_name": "Product Name",
        "product": "Product Name",
        "category": "Category",
        "region": "Region",
        "quantity": "Quantity",
        "qty": "Quantity",
        "unit price": "Unit Price",
        "unit_price": "Unit Price",
        "price": "Unit Price",
        "total sales": "Total Sales",
        "total_sales": "Total Sales",
        "sales": "Total Sales",
        "revenue": "Total Sales",
        "cost": "Cost",
        "total cost": "Cost",
        "profit": "Profit",
        "net profit": "Profit"
    }

    renamed = {}
    for col in df.columns:
        clean_key = str(col).strip().lower()
        if clean_key in mapping:
            renamed[col] = mapping[clean_key]
        else:
            renamed[col] = str(col).strip()

    return df.rename(columns=renamed)


def clean_sales_dataset(
    df: pd.DataFrame,
    handle_missing_strategy: str = "impute",
    drop_duplicates_flag: bool = True,
    recalculate_metrics: bool = True
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Comprehensive data cleaning pipeline for sales datasets.

    Args:
        df (pd.DataFrame): Raw sales DataFrame.
        handle_missing_strategy (str): 'impute' (mean/mode), 'drop', or 'none'.
        drop_duplicates_flag (bool): Whether to remove duplicate rows.
        recalculate_metrics (bool): Recompute Total Sales & Profit strictly.

    Returns:
        Tuple[pd.DataFrame, Dict[str, Any]]: Cleaned DataFrame and log report.
    """
    if df is None or df.empty:
        return pd.DataFrame(), {"status": "Empty DataFrame provided"}

    cleaned_df = df.copy()
    cleaned_df = standardize_columns(cleaned_df)

    log = {
        "initial_rows": len(cleaned_df),
        "duplicates_removed": 0,
        "missing_values_handled": 0,
        "date_parsed": False,
        "recalculated_metrics": False
    }

    # 1. Remove duplicate records
    if drop_duplicates_flag:
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        if "Order ID" in cleaned_df.columns:
            cleaned_df = cleaned_df.drop_duplicates(subset=["Order ID"])
        log["duplicates_removed"] = initial_count - len(cleaned_df)

    # 2. Date conversion
    if "Order Date" in cleaned_df.columns:
        cleaned_df["Order Date"] = pd.to_datetime(cleaned_df["Order Date"], errors="coerce")
        # Fill missing dates with most frequent or current date if needed
        if cleaned_df["Order Date"].isnull().any():
            cleaned_df["Order Date"] = cleaned_df["Order Date"].fillna(pd.Timestamp.today().normalize())
        log["date_parsed"] = True

    # 3. Numeric column parsing
    numeric_cols = ["Quantity", "Unit Price", "Total Sales", "Cost", "Profit"]
    for col in numeric_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")

    # 4. Handle Missing Values
    initial_nulls = int(cleaned_df.isnull().sum().sum())
    
    if handle_missing_strategy == "drop":
        cleaned_df = cleaned_df.dropna().reset_index(drop=True)
        log["missing_values_handled"] = initial_nulls
    elif handle_missing_strategy == "impute":
        for col in cleaned_df.columns:
            if cleaned_df[col].isnull().any():
                if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                    median_val = cleaned_df[col].median()
                    cleaned_df[col] = cleaned_df[col].fillna(median_val if not pd.isna(median_val) else 0)
                elif pd.api.types.is_datetime64_any_dtype(cleaned_df[col]):
                    cleaned_df[col] = cleaned_df[col].fillna(pd.Timestamp.today().normalize())
                else:
                    mode_val = cleaned_df[col].mode()
                    fill_val = mode_val[0] if not mode_val.empty else "Unknown"
                    cleaned_df[col] = cleaned_df[col].fillna(fill_val)
        log["missing_values_handled"] = initial_nulls

    # 5. String strip & fill for categoricals
    categorical_cols = ["Customer Name", "Product Name", "Category", "Region"]
    for col in categorical_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            cleaned_df[col] = cleaned_df[col].replace({"nan": "Unknown", "None": "Unknown", "": "Unknown"})

    # 6. Recalculate and guarantee business formula integrity:
    # Total Sales = Quantity * Unit Price
    # Profit = Total Sales - Cost
    if recalculate_metrics:
        if "Quantity" in cleaned_df.columns:
            cleaned_df["Quantity"] = cleaned_df["Quantity"].round().astype(int)
        
        if "Quantity" in cleaned_df.columns and "Unit Price" in cleaned_df.columns:
            cleaned_df["Total Sales"] = (cleaned_df["Quantity"] * cleaned_df["Unit Price"]).round(2)
        
        if "Total Sales" in cleaned_df.columns and "Cost" in cleaned_df.columns:
            cleaned_df["Profit"] = (cleaned_df["Total Sales"] - cleaned_df["Cost"]).round(2)
            
        log["recalculated_metrics"] = True

    cleaned_df = cleaned_df.reset_index(drop=True)
    log["final_rows"] = len(cleaned_df)

    return cleaned_df, log
