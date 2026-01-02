# ==========================================================
# FLEXIMART – FINAL ETL PIPELINE
# Customers + Products + Sales
# ==========================================================

import pandas as pd
from dateutil import parser
import mysql.connector
from datetime import datetime

# ==========================================================
# DATA QUALITY METRICS (GLOBAL)
# ==========================================================
report = {
    "customers": {"read": 0, "duplicates": 0, "missing": 0, "loaded": 0},
    "products": {"read": 0, "duplicates": 0, "missing": 0, "loaded": 0},
    "sales": {"read": 0, "duplicates": 0, "missing": 0, "loaded": 0},
}

# ==========================================================
# MYSQL CONNECTION (SINGLE)
# ==========================================================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7674",      
    database="fleximart"
)
cursor = conn.cursor()
print("Connected to MySQL")

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def clean_phone(phone):
    phone = str(phone).strip().replace("-", "").replace(" ", "")
    if phone.startswith("0"):
        phone = phone[1:]
    if phone.isdigit() and len(phone) == 10:
        return "+91" + phone
    if phone.startswith("+91"):
        return phone
    return None

def clean_date(val):
    try:
        return parser.parse(str(val), dayfirst=True).date()
    except:
        return None

# ==========================================================
# ================= CUSTOMER ETL ===========================
# ==========================================================
print("\n--- CUSTOMER ETL STARTED ---")

customers = pd.read_csv("data/customers_raw.csv", header=None)
customers = customers[0].str.split(",", expand=True)

customers.columns = [
    "customer_id", "first_name", "last_name",
    "email", "phone", "city", "registration_date"
]

report["customers"]["read"] = len(customers)

# Remove header row
customers = customers[customers["customer_id"] != "customer_id"]

# Remove duplicates
before = len(customers)
customers = customers.drop_duplicates()
report["customers"]["duplicates"] = before - len(customers)

# Remove missing emails
before = len(customers)
customers = customers.dropna(subset=["email"])
customers = customers[customers["email"] != ""]
report["customers"]["missing"] = before - len(customers)

# Clean fields
customers["phone"] = customers["phone"].apply(clean_phone)
customers["city"] = customers["city"].str.strip().str.title()
customers["registration_date"] = customers["registration_date"].apply(clean_date)

# Insert safely
customer_insert = """
INSERT IGNORE INTO customers
(first_name, last_name, email, phone, city, registration_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in customers.iterrows():
    cursor.execute(customer_insert, (
        row["first_name"], row["last_name"],
        row["email"], row["phone"],
        row["city"], row["registration_date"]
    ))

conn.commit()
report["customers"]["loaded"] = len(customers)
print("Customers loaded:", len(customers))

# ==========================================================
# ================= PRODUCT ETL ============================
# ==========================================================
print("\n--- PRODUCT ETL STARTED ---")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0
)
""")
conn.commit()
cursor.execute("DELETE FROM products")
conn.commit()


products = pd.read_csv("data/products_raw.csv", header=None)
if products.shape[1] == 1:
    products = products[0].str.split(",", expand=True)

products.columns = ["pid", "product_name", "category", "price", "stock_quantity"]
products = products.iloc[1:]

report["products"]["read"] = len(products)

# Clean
products["product_name"] = products["product_name"].str.strip()
products["category"] = products["category"].str.strip().str.title()
products["price"] = pd.to_numeric(products["price"], errors="coerce")
before = len(products)
products = products.dropna(subset=["price"])
report["products"]["missing"] = before - len(products)

products["stock_quantity"] = (
    products["stock_quantity"]
    .fillna(0).astype(str)
    .str.replace(".0", "", regex=False)
    .apply(lambda x: int(x) if x.isdigit() else 0)
)

product_insert = """
INSERT INTO products (product_name, category, price, stock_quantity)
VALUES (%s, %s, %s, %s)
"""

for _, row in products.iterrows():
    cursor.execute(product_insert, (
        row["product_name"], row["category"],
        float(row["price"]), row["stock_quantity"]
    ))

conn.commit()
report["products"]["loaded"] = len(products)
print("Products loaded:", len(products))

# ==========================================================
# ================= SALES ETL ==============================
# ==========================================================
print("\n--- SALES ETL STARTED ---")

sales = pd.read_csv("data/sales_raw.csv", header=None)
if sales.shape[1] == 1:
    sales = sales[0].str.split(",", expand=True)

sales.columns = [
    "transaction_id", "customer_id", "product_id",
    "quantity", "unit_price", "transaction_date", "status"
]

report["sales"]["read"] = len(sales)

sales = sales[sales["transaction_id"] != "transaction_id"]

# Deduplicate
before = len(sales)
sales = sales.drop_duplicates(subset=["transaction_id"])
report["sales"]["duplicates"] = before - len(sales)

# Remove missing IDs
before = len(sales)
sales = sales.dropna(subset=["customer_id", "product_id"])
sales = sales[(sales["customer_id"] != "") & (sales["product_id"] != "")]
report["sales"]["missing"] = before - len(sales)

# Clean
sales["transaction_date"] = sales["transaction_date"].apply(clean_date)
sales = sales.dropna(subset=["transaction_date"])
sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce").fillna(0).astype(int)
sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce")
sales = sales.dropna(subset=["unit_price"])
sales["status"] = sales["status"].str.strip().str.title()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(20),
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INT,
    unit_price DECIMAL(10,2),
    transaction_date DATE,
    status VARCHAR(20)
)
""")
conn.commit()
cursor.execute("DELETE FROM sales")
conn.commit()


insert_sales = """
INSERT INTO sales
(transaction_id, customer_id, product_id, quantity,
 unit_price, transaction_date, status)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for _, row in sales.iterrows():
    cursor.execute(insert_sales, (
        row["transaction_id"], row["customer_id"], row["product_id"],
        row["quantity"], float(row["unit_price"]),
        row["transaction_date"], row["status"]
    ))

conn.commit()
report["sales"]["loaded"] = len(sales)
print("Sales loaded:", len(sales))

# ==========================================================
# ============ DATA QUALITY REPORT =========================
# ==========================================================
with open("data_quality_report.txt", "w") as f:
    f.write("FLEXIMART DATA QUALITY REPORT\n")
    f.write(f"Generated on: {datetime.now()}\n\n")

    for table, stats in report.items():
        f.write(f"{table.upper()} DATA\n")
        f.write(f"Records read: {stats['read']}\n")
        f.write(f"Duplicates removed: {stats['duplicates']}\n")
        f.write(f"Missing values handled: {stats['missing']}\n")
        f.write(f"Records loaded: {stats['loaded']}\n")
        f.write("-" * 30 + "\n")

cursor.close()
conn.close()
print("\nETL PIPELINE COMPLETED SUCCESSFULLY")
