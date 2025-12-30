# FLEXIMART DATABASE SCHEMA DOCUMENTATION

## Overview
This document describes the database schema used in the FlexiMart ETL pipeline.  
The schema is designed to store cleaned customer, product, and sales transaction data
loaded via the ETL process.

---

## 1. Entity–Relationship Description

### ENTITY: customers
**Purpose:** Stores customer master information.

**Attributes:**
- customer_id (INT, Primary Key, Auto Increment): Unique customer identifier
- first_name (VARCHAR): Customer first name
- last_name (VARCHAR): Customer last name
- email (VARCHAR): Customer email address (unique)
- phone (VARCHAR): Standardized phone number (+91 format)
- city (VARCHAR): City of residence
- registration_date (DATE): Date customer registered

**Relationships:**
- One customer can place MANY sales transactions  
  (1 → M relationship with `sales` table)

---

### ENTITY: products
**Purpose:** Stores product catalog details.

**Attributes:**
- product_id (INT, Primary Key, Auto Increment): Unique product identifier
- product_name (VARCHAR): Name of the product
- category (VARCHAR): Standardized product category
- price (DECIMAL): Product unit price
- stock_quantity (INT): Available stock quantity

**Relationships:**
- One product can appear in MANY sales transactions  
  (1 → M relationship with `sales` table)

---

### ENTITY: sales
**Purpose:** Stores transactional sales records.

**Attributes:**
- id (INT, Primary Key, Auto Increment): Surrogate key
- transaction_id (VARCHAR): Business transaction identifier
- customer_id (VARCHAR): References customer making the purchase
- product_id (VARCHAR): References product sold
- quantity (INT): Quantity purchased
- unit_price (DECIMAL): Price per unit at time of sale
- transaction_date (DATE): Date of transaction
- status (VARCHAR): Transaction status (Completed, Pending, Cancelled)

**Relationships:**
- MANY sales belong to ONE customer
- MANY sales belong to ONE product

---

## 2. Normalization Explanation (3NF)

The FlexiMart database schema follows Third Normal Form (3NF).

**First Normal Form (1NF):**
- All tables contain atomic values.
- No repeating groups or multi-valued attributes exist.
- Each row is uniquely identifiable by a primary key.

**Second Normal Form (2NF):**
- All non-key attributes are fully dependent on the primary key.
- No partial dependency exists because surrogate primary keys are used.

**Third Normal Form (3NF):**
- No transitive dependencies exist.
- Customer details are stored only in the `customers` table.
- Product details are stored only in the `products` table.
- Sales table only stores transaction-specific attributes.

**Anomaly Prevention:**
- Update anomalies avoided by separating master data.
- Insert anomalies avoided by allowing independent entity creation.
- Delete anomalies avoided because transactions do not delete master data.

---

## 3. Sample Data Representation

### customers (sample)

| customer_id | first_name | email              | city     |
|------------|-----------|--------------------|----------|
| 1 | Suresh | suresh.patel@outlook.com | Mumbai |
| 2 | Neha | neha.shah@gmail.com | Ahmedabad |

---

### products (sample)

| product_id | product_name | category | price |
|-----------|--------------|---------|-------|
| 1 | Samsung Galaxy S21 | Electronics | 45999 |
| 2 | Nike Running Shoes | Fashion | 3499 |

---

### sales (sample)

| transaction_id | customer_id | product_id | quantity | transaction_date |
|---------------|------------|-----------|----------|------------------|
| T001 | C001 | P001 | 1 | 2024-01-15 |
| T002 | C002 | P004 | 2 | 2024-01-16 |

---

## End of Schema Documentation
