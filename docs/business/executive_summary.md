# Executive Summary - Commercial-Alfa BI Platform

## Project Overview
This project establishes a modern Business Intelligence (BI) infrastructure for the cosmetics sales vertical. The primary objective was to decouple a flat and coupled data file (`cosmetics_sales_data.csv`) and transform it into a robust Data Mart based on Ralph Kimball's *Star Schema* dimensional modeling.

## Solution Architecture
* **Storage Layer:** Local PostgreSQL serving as the Data Warehouse.
* **ETL Pipeline:** Automated processing via Python (Pandas + Psycopg2) with atomic injection via Bulk Insert.
* **Visualization Layer:** Cross-platform analytical dashboards programmatically generated via Python (Matplotlib + Seaborn) on macOS, emulating Power BI metrics and exporting high-resolution interface captures directly into the repository structure.
