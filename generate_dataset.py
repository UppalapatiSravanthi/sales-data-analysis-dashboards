"""
Sales Dataset Generator
-----------------------
Generates a realistic sample sales dataset of 1,200+ records.
Includes products across multiple categories, realistic pricing,
quantities, costs, regional distributions, and customer names.

Columns:
- Order ID
- Order Date
- Customer Name
- Product Name
- Category
- Region
- Quantity
- Unit Price
- Total Sales (Quantity * Unit Price)
- Cost
- Profit (Total Sales - Cost)
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def generate_sales_data(num_records: int = 1250, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic, realistic sales transaction data.
    
    Args:
        num_records (int): Number of order records to generate (minimum 1000).
        seed (int): Random seed for reproducibility.
        
    Returns:
        pd.DataFrame: Cleaned synthetic sales dataset.
    """
    random.seed(seed)
    np.random.seed(seed)

    # Master product catalog with base categories and typical unit prices
    product_catalog = [
        # Electronics
        {"product": "Dell XPS 15 Laptop", "category": "Electronics", "unit_price": 1499.99, "cost_ratio": 0.72},
        {"product": "Apple MacBook Air M2", "category": "Electronics", "unit_price": 1199.00, "cost_ratio": 0.75},
        {"product": "Samsung 34-Inch Curved Monitor", "category": "Electronics", "unit_price": 549.50, "cost_ratio": 0.68},
        {"product": "Sony WH-1000XM5 Headphones", "category": "Electronics", "unit_price": 379.99, "cost_ratio": 0.65},
        {"product": "Logitech 4K Pro Webcam", "category": "Electronics", "unit_price": 199.99, "cost_ratio": 0.60},
        {"product": "HP LaserJet Pro Multifunction Printer", "category": "Electronics", "unit_price": 329.00, "cost_ratio": 0.70},
        {"product": "Anker 10-in-1 USB-C Hub", "category": "Electronics", "unit_price": 89.99, "cost_ratio": 0.55},
        
        # Furniture
        {"product": "Ergonomic Mesh Office Chair", "category": "Furniture", "unit_price": 289.00, "cost_ratio": 0.62},
        {"product": "Motorized Standing Desk 60x30", "category": "Furniture", "unit_price": 499.00, "cost_ratio": 0.66},
        {"product": "Executive High-Back Leather Chair", "category": "Furniture", "unit_price": 349.00, "cost_ratio": 0.64},
        {"product": "Solid Oak Conference Table", "category": "Furniture", "unit_price": 890.00, "cost_ratio": 0.70},
        {"product": "5-Tier Industrial Bookshelf", "category": "Furniture", "unit_price": 185.00, "cost_ratio": 0.58},
        {"product": "Mobile 3-Drawer File Cabinet", "category": "Furniture", "unit_price": 145.00, "cost_ratio": 0.60},
        
        # Office Supplies
        {"product": "Heavy-Duty Cross-Cut Shredder", "category": "Office Supplies", "unit_price": 129.99, "cost_ratio": 0.63},
        {"product": "Premium Multipurpose Copy Paper (10 Reams)", "category": "Office Supplies", "unit_price": 54.50, "cost_ratio": 0.78},
        {"product": "Ergonomic Keyboard Wrist Rest Set", "category": "Office Supplies", "unit_price": 29.99, "cost_ratio": 0.45},
        {"product": "Commercial Heavy-Duty Stapler Set", "category": "Office Supplies", "unit_price": 34.90, "cost_ratio": 0.50},
        {"product": "Magnetic Whiteboard 48x36", "category": "Office Supplies", "unit_price": 95.00, "cost_ratio": 0.58},
        {"product": "Dry Erase Marker 24-Color Pack", "category": "Office Supplies", "unit_price": 19.99, "cost_ratio": 0.42},
        {"product": "Self-Adhesive Sticky Notes Bulk Box", "category": "Office Supplies", "unit_price": 24.50, "cost_ratio": 0.40},
        
        # Accessories
        {"product": "Logitech MX Master 3S Wireless Mouse", "category": "Accessories", "unit_price": 99.99, "cost_ratio": 0.58},
        {"product": "Keychron Mechanical Wireless Keyboard", "category": "Accessories", "unit_price": 119.00, "cost_ratio": 0.60},
        {"product": "Aluminum Laptop Stand Riser", "category": "Accessories", "unit_price": 45.00, "cost_ratio": 0.48},
        {"product": "Fast Wireless Charging Pad 15W", "category": "Accessories", "unit_price": 32.50, "cost_ratio": 0.52},
        {"product": "Surge Protector 12-Outlet Power Strip", "category": "Accessories", "unit_price": 38.00, "cost_ratio": 0.50}
    ]

    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
        "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
        "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
    ]

    regions = ["North", "South", "East", "West", "Central"]
    region_weights = [0.22, 0.18, 0.26, 0.24, 0.10]

    # Pre-generate unique customer pool of 120 individuals
    customers = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(120)]
    customers = list(dict.fromkeys(customers)) # remove duplicates

    # Date generation between 2023-01-01 and 2024-12-31 (2 full operating years)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{10000 + i}"
        
        # Random date with slight end-of-year seasonal weight (Q4 sales boost)
        day_offset = random.randint(0, total_days)
        order_date = start_date + timedelta(days=day_offset)
        
        customer_name = random.choice(customers)
        prod = random.choice(product_catalog)
        product_name = prod["product"]
        category = prod["category"]
        
        region = random.choices(regions, weights=region_weights)[0]
        
        # Quantity purchased: typically 1 to 5, occasionally larger for bulk supplies
        if category in ["Office Supplies", "Accessories"]:
            quantity = random.choices([1, 2, 3, 4, 5, 6, 8, 10], weights=[0.25, 0.25, 0.20, 0.12, 0.08, 0.05, 0.03, 0.02])[0]
        else:
            quantity = random.choices([1, 2, 3, 4], weights=[0.60, 0.25, 0.10, 0.05])[0]
            
        unit_price = prod["unit_price"]
        total_sales = round(quantity * unit_price, 2)
        
        # Cost modeling: base cost ratio + slight random variance (-5% to +8%)
        # Occasionally a small clearance or seasonal discount lowers profit or causes slight loss
        cost_variance = random.uniform(-0.04, 0.08)
        cost_ratio = min(max(prod["cost_ratio"] + cost_variance, 0.35), 0.95)
        
        # 3% chance of a special clearance item having high cost (slight loss or break-even)
        if random.random() < 0.03:
            cost_ratio = random.uniform(1.01, 1.08)

        cost = round(total_sales * cost_ratio, 2)
        profit = round(total_sales - cost, 2)

        records.append({
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Customer Name": customer_name,
            "Product Name": product_name,
            "Category": category,
            "Region": region,
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Total Sales": total_sales,
            "Cost": cost,
            "Profit": profit
        })

    df = pd.DataFrame(records)
    
    # Sort chronologically by Order Date
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df = df.sort_values(by="Order Date").reset_index(drop=True)
    df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")
    
    return df


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_dir = os.path.join(base_dir, "datasets")
    os.makedirs(datasets_dir, exist_ok=True)

    csv_path = os.path.join(datasets_dir, "sales_data.csv")
    print("Generating synthetic sales dataset (1,250 records)...")
    df = generate_sales_data(num_records=1250)
    
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully created and saved to: {csv_path}")
    print(f"Total Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Total Sales: ${df['Total Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")

    # Initialize SQLite database if database module is available
    try:
        from database import init_db, save_to_database
        db_path = os.path.join(base_dir, "sales.db")
        init_db(db_path)
        inserted, skipped = save_to_database(df, db_path)
        print(f"Populated SQLite Database ({db_path}): {inserted} records inserted, {skipped} skipped.")
    except Exception as e:
        print(f"Database sync note: {e}")


if __name__ == "__main__":
    main()
