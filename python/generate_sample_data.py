import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sample_sales_data.csv"

random.seed(42)

categories = ["Electronics", "Office Supplies", "Furniture", "Software", "Books"]
regions = ["Tokyo", "Osaka", "Nagoya", "Fukuoka", "Sapporo"]
products = {
    "Electronics": ["Keyboard", "Mouse", "Monitor", "Webcam"],
    "Office Supplies": ["Notebook", "Pen Set", "File Folder", "Copy Paper"],
    "Furniture": ["Desk", "Office Chair", "Bookshelf"],
    "Software": ["Security Tool", "Accounting App", "Design Tool"],
    "Books": ["Business Book", "Programming Book", "Design Book"]
}

start_date = datetime(2025, 1, 1)
rows = []

for i in range(1, 2001):
    order_date = start_date + timedelta(days=random.randint(0, 364))
    category = random.choice(categories)
    product = random.choice(products[category])
    quantity = random.randint(1, 10)
    unit_price = random.randint(500, 30000)

    # Add a simple seasonal trend
    month = order_date.month
    trend_multiplier = 1.0
    if month in [3, 4, 11, 12]:
        trend_multiplier = 1.25
    elif month in [7, 8]:
        trend_multiplier = 0.85

    amount = int(quantity * unit_price * trend_multiplier)

    rows.append({
        "Order ID": f"ORD-{i:05d}",
        "Order Date": order_date.strftime("%Y-%m-%d"),
        "Customer ID": f"C{random.randint(1, 300):04d}",
        "Region": random.choice(regions),
        "Category": category,
        "Product Name": product,
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Amount": amount
    })

df = pd.DataFrame(rows)
df.to_csv(DATA_PATH, index=False)

print(f"Sample data created: {DATA_PATH}")
print(f"Rows: {len(df)}")
