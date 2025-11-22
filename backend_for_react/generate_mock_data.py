# generate_mock_data.py
import json
import os
import random
from datetime import datetime, timedelta, timezone

# Step 1: Generate mock customer data
customers = []
for i in range(1, 11):
    customers.append({
        "customer_id": f"C{i:03}",
        "name": f"Customer {i}"
    })

# Step 2: Generate mock product data
products = []
# Products will now include price and cost
for i in range(1, 11):
    base_price = round(random.uniform(20.00, 100.00), 2)
    cost = round(base_price * random.uniform(0.3, 0.6), 2) # Cost is 30-60% of price
    products.append({
        "product_id": f"P{i:03}",
        "name": f"Product {i}",
        "stock_level": random.randint(10, 200),
        "price": base_price,
        "cost": cost
    })

# Step 3: Generate mock purchase records
purchases = []
customer_ids = [c["customer_id"] for c in customers]
product_details = {p["product_id"]: p for p in products} # For quick price lookup
product_keys = list(product_details.keys())  # Cache keys outside loop

start_date = datetime.now(timezone.utc) - timedelta(days=30)

for i in range(50):
    purchase_timestamp = start_date + timedelta(days=random.uniform(0, 30))
    chosen_product_id = random.choice(product_keys)

    purchases.append({
        "purchase_id": f"PUR{i:03}", # Changed from sale_id for consistency
        "customer_id": random.choice(customer_ids),
        "product_id": chosen_product_id,
        "quantity": random.randint(1, 5),
        "price": product_details[chosen_product_id]['price'], # Get price from product details
        "timestamp": purchase_timestamp.isoformat()
    })

# Step 4: Generate mock expenses
expenses = [
    {"expense_id": "E001", "description": "Office Rent", "amount": 800.00},
    {"expense_id": "E002", "description": "Marketing Campaign", "amount": 300.00},
    {"expense_id": "E003", "description": "Utilities", "amount": 150.00},
    {"expense_id": "E004", "description": "Software Subscriptions", "amount": 120.00},
]

# Step 5: Combine into a single JSON object
data = {
    "customers": customers,
    "products": products,
    "purchases": purchases,
    "expenses": expenses
}

# Step 6: Save to data.json file inside the 'data' subfolder
try:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "data.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Mock data has been successfully generated and saved to {file_path}")
except (IOError, OSError) as e:
    print(f"Error saving data: {e}")
    raise

