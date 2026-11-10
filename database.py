"""
Database Management Module
--------------------------
Handles all SQLite operations for the Sales Analysis Dashboard:
- Initializing database schema
- Storing new/uploaded records while preventing duplicate Order IDs
- Fetching historical sales records into Pandas DataFrames
- Calculating quick database statistics
"""

import sqlite3
import os
import pandas as pd
from typing import Tuple, Dict, Any


DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales.db")


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Initialize SQLite database schema.
    Creates the 'sales' table with Order ID as a UNIQUE constraint
    to strictly prevent duplicate transactions.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL UNIQUE,
            order_date TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_sales REAL NOT NULL,
            cost REAL NOT NULL,
            profit REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create indexes for high-speed filtering and aggregation
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales(category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON sales(region);")
    
    conn.commit()
    conn.close()


def save_to_database(df: pd.DataFrame, db_path: str = DEFAULT_DB_PATH) -> Tuple[int, int]:
    """
    Save records from a Pandas DataFrame into the SQLite database.
    Avoids duplicate entries by checking existing Order IDs.

    Args:
        df (pd.DataFrame): DataFrame containing sales records.
        db_path (str): Path to SQLite database file.

    Returns:
        Tuple[int, int]: (number_of_records_inserted, number_of_duplicates_skipped)
    """
    if df is None or df.empty:
        return 0, 0

    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Normalize incoming column names
    col_mapping = {
        "order id": "order_id",
        "order_id": "order_id",
        "order date": "order_date",
        "order_date": "order_date",
        "customer name": "customer_name",
        "customer_name": "customer_name",
        "product name": "product_name",
        "product_name": "product_name",
        "category": "category",
        "region": "region",
        "quantity": "quantity",
        "unit price": "unit_price",
        "unit_price": "unit_price",
        "total sales": "total_sales",
        "total_sales": "total_sales",
        "cost": "cost",
        "profit": "profit"
    }

    df_clean = df.copy()
    renamed_cols = {}
    for col in df_clean.columns:
        norm = str(col).strip().lower()
        if norm in col_mapping:
            renamed_cols[col] = col_mapping[norm]
            
    df_clean = df_clean.rename(columns=renamed_cols)

    # Ensure required columns exist
    required = ["order_id", "order_date", "customer_name", "product_name", 
                "category", "region", "quantity", "unit_price", "total_sales", "cost", "profit"]
    
    missing = [c for c in required if c not in df_clean.columns]
    if missing:
        conn.close()
        raise ValueError(f"Missing required columns in dataset: {missing}")

    # Fetch existing order IDs to prevent duplicate inserts
    cursor.execute("SELECT order_id FROM sales;")
    existing_ids = {row[0] for row in cursor.fetchall()}

    records_to_insert = []
    skipped = 0

    for _, row in df_clean.iterrows():
        oid = str(row["order_id"]).strip()
        if oid in existing_ids:
            skipped += 1
            continue
        
        # Format date as YYYY-MM-DD
        raw_date = row["order_date"]
        if pd.notnull(raw_date):
            date_str = pd.to_datetime(raw_date).strftime("%Y-%m-%d")
        else:
            date_str = ""

        records_to_insert.append((
            oid,
            date_str,
            str(row["customer_name"]).strip(),
            str(row["product_name"]).strip(),
            str(row["category"]).strip(),
            str(row["region"]).strip(),
            int(row["quantity"]),
            float(row["unit_price"]),
            float(row["total_sales"]),
            float(row["cost"]),
            float(row["profit"])
        ))
        existing_ids.add(oid)

    if records_to_insert:
        cursor.executemany("""
            INSERT OR IGNORE INTO sales (
                order_id, order_date, customer_name, product_name,
                category, region, quantity, unit_price, total_sales,
                cost, profit
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, records_to_insert)
        conn.commit()

    inserted = len(records_to_insert)
    conn.close()
    return inserted, skipped


def load_from_database(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """
    Retrieve historical sales data from the SQLite database.

    Returns:
        pd.DataFrame: Formatted sales DataFrame with user-friendly column names.
    """
    if not os.path.exists(db_path):
        init_db(db_path)
        return pd.DataFrame()

    conn = get_connection(db_path)
    query = """
        SELECT 
            order_id AS 'Order ID',
            order_date AS 'Order Date',
            customer_name AS 'Customer Name',
            product_name AS 'Product Name',
            category AS 'Category',
            region AS 'Region',
            quantity AS 'Quantity',
            unit_price AS 'Unit Price',
            total_sales AS 'Total Sales',
            cost AS 'Cost',
            profit AS 'Profit'
        FROM sales
        ORDER BY order_date ASC;
    """
    try:
        df = pd.read_sql_query(query, conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()

    if not df.empty:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
        df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce").fillna(0.0)
        df["Total Sales"] = pd.to_numeric(df["Total Sales"], errors="coerce").fillna(0.0)
        df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce").fillna(0.0)
        df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0.0)

    return df


def get_table_summary(db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """Return summary metadata regarding the current database state."""
    if not os.path.exists(db_path):
        return {"total_records": 0, "first_date": None, "last_date": None, "total_sales": 0.0}

    conn = get_connection(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*), MIN(order_date), MAX(order_date), SUM(total_sales) FROM sales;")
        row = cursor.fetchone()
        return {
            "total_records": row[0] or 0,
            "first_date": row[1],
            "last_date": row[2],
            "total_sales": round(row[3] or 0.0, 2)
        }
    except sqlite3.OperationalError:
        return {"total_records": 0, "first_date": None, "last_date": None, "total_sales": 0.0}
    finally:
        conn.close()


def clear_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """Empty all records from the sales table."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales;")
    conn.commit()
    conn.close()


def get_active_dataset(db_path: str = DEFAULT_DB_PATH, csv_fallback: str = None) -> pd.DataFrame:
    """
    Convenience loader that returns the active dataset:
    1. Loads from SQLite database if populated.
    2. If SQLite is empty, falls back to datasets/sales_data.csv and auto-populates SQLite.
    3. If neither exists, generates sample data and saves both to CSV and SQLite.
    """
    df = load_from_database(db_path)
    if not df.empty:
        return df

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if csv_fallback is None:
        csv_fallback = os.path.join(base_dir, "datasets", "sales_data.csv")

    if os.path.exists(csv_fallback):
        df_csv = pd.read_csv(csv_fallback)
        save_to_database(df_csv, db_path)
        return load_from_database(db_path)

    # If CSV doesn't exist yet, generate it on the fly
    from generate_dataset import generate_sales_data
    os.makedirs(os.path.dirname(csv_fallback), exist_ok=True)
    df_gen = generate_sales_data(1250)
    df_gen.to_csv(csv_fallback, index=False)
    save_to_database(df_gen, db_path)
    return load_from_database(db_path)

