# FlexiMart Data Architecture Project

**Student Name:** Abhyuday Mishra  
**Student ID:** [bitsom_ba_2507632]  
**Email:** [abhyudaymishra7674@gmail.com]  
**Date:** 31 December 2025

---

## Project Overview

The FlexiMart Data Architecture Project demonstrates an end-to-end data engineering workflow covering ETL processing, NoSQL data modeling, and data warehousing with OLAP analytics. The project transforms raw retail data into structured analytical models to support business intelligence and decision-making using SQL and MongoDB.

The implementation is divided into three parts: relational ETL and data quality handling, NoSQL analysis using MongoDB, and a star-schema-based data warehouse with analytical queries.

---

## Repository Structure
abhyuday-fleximart-data-architecture/
├── README.md
├── .gitignore
├── data/
│ ├── customers_raw.csv
│ ├── products_raw.csv
│ └── sales_raw.csv
│
├── part1-database-etl/
│ ├── README.md
│ ├── etl_pipeline.py
│ ├── schema_documentation.md
│ ├── business_queries.sql
│ ├── data_quality_report.txt
│ └── requirements.txt
│
├── part2-nosql/
│ ├── README.md
│ ├── nosql_analysis.md
│ ├── mongodb_operations.js
│ └── products_catalog.json
│
└── part3-datawarehouse/
├── README.md
├── star_schema_design.md
├── warehouse_schema.sql
├── warehouse_data.sql
└── analytics_queries.sql
└── README.md

---

## Technologies Used

- **Python 3.x** – ETL pipeline development  
- **pandas** – Data cleaning and transformation  
- **MySQL 8.0** – Relational database and data warehouse  
- **MongoDB 6.0** – NoSQL document-based data modeling  
- **SQL** – Data definition, manipulation, and OLAP analytics  

---

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql

---

## MongoDB Setup
mongosh < part2-nosql/mongodb_operations.js

---

## Key Learnings
This project provided hands-on experience in designing and implementing ETL pipelines and enforcing data quality checks. It improved understanding of when to use relational databases, NoSQL databases, and data warehouses. The project also strengthened SQL skills for both operational and analytical workloads and demonstrated the importance of proper data modeling for business intelligence.

---

## Challenges Faced

1. Data Quality and Inconsistent Records
This was resolved by implementing validation rules and generating a data quality report during the ETL process.
2. Designing Schemas for Multiple Data Models
This challenge was addressed by applying normalization for relational databases, document-based modeling for MongoDB, and star schema design for the data warehouse.







